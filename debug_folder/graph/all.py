import logging
from abc import ABC, abstractmethod
import json
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from threading import Lock
from collections import defaultdict


# 配置日志记录
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# 定义抽象基类NodeBase
class NodeBase(ABC):
    def __init__(self, node_name):
        self.node_name = node_name
        self.impl_type = 'io'

    def log(self, message, level=logging.INFO):
        """记录日志信息"""
        class_name = self.__class__.__name__
        prefix = f"[{class_name}::{self.node_name}] "
        logger.log(level, prefix + message)

    def raise_error(self, message):
        """统一构建异常信息并引发错误"""
        self.log(message, level=logging.ERROR)
        raise ValueError(message)

    @abstractmethod
    def process(self, data):
        """抽象方法，需在子类中实现具体的处理逻辑"""
        pass

    def run(self, data):
        """运行节点的process方法，并记录输入输出"""
        try:
            self.log(f"Processing input data: {data}")
            result = self.process(data)
            self.log(f"Output data: {result}")
            return result  # 只返回结果，不存储
        except Exception as e:
            self.log(f"An error occurred: {e}", level=logging.ERROR)
            raise

# 输入节点，从用户获取输入数据
class InputNode(NodeBase):
    def __init__(self, node_name):
        super().__init__(node_name)
        self.impl_type = 'io'
    def process(self, data):
        # 假设data是用户的输入
        return data

# 计算输入数据长度的节点
class LengthNode(NodeBase):
    def __init__(self, node_name):
        super().__init__(node_name)
        self.impl_type = 'cpu'
    def process(self, data):
        return len(data[0])

# 获取输入数据第一个字符的节点
class FirstCharNode(NodeBase):
    def __init__(self, node_name):
        super().__init__(node_name)
        self.impl_type = 'io'
    def process(self, data):
        return data[0][0] if data else None

# 将多个依赖节点的数据连接起来的节点
class ConcatNode(NodeBase):

    def process(self, data):
        out = ""
        for i in data:
            out += str(i) if i else ""
        return out

# 定义DAG类，用于解析JSON配置和执行节点
class DAG:
    def __init__(self, config):
        self.config = config
        self.nodes = {}
        self.dependencies = {}
        self.data_structure = {}
        self.nodes_depend_on_mapskey = defaultdict(list)
        self.load_nodes()

    def load_nodes(self):
        """加载节点配置，实例化节点对象"""
        for node_config in self.config['nodes']:
            name = node_config['name']
            impl = globals()[node_config['impl']]
            node = impl(name)
            self.nodes[name] = node
            self.dependencies[name] = node_config.get('deps', [])
            for dep in self.dependencies[name]:
                self.nodes_depend_on_mapskey[dep].append(name)

    def topological_sort(self):
        """拓扑排序，确保节点按依赖顺序执行"""
        indegree = {node: 0 for node in self.nodes}
        for deps in self.dependencies.values():
            for dep in deps:
                indegree[dep] += 1

        queue = [node for node in self.nodes if indegree[node] == 0]
        sorted_nodes = []

        while queue:
            node = queue.pop(0)
            sorted_nodes.append(node)
            for dep in self.dependencies[node]:
                indegree[dep] -= 1
                if indegree[dep] == 0:
                    queue.append(dep)

        if len(sorted_nodes) != len(self.nodes):
            raise ValueError("Graph has cycles")

        return sorted_nodes
    
    def execute_node(self, node_name, initial_input):
        
        node = self.nodes[node_name]
        deps_data = [self.data_structure[dep] for dep in self.dependencies[node_name]]
        print(node_name, self.data_structure, deps_data)
        return node.run(deps_data if deps_data else initial_input)

    def run(self, initial_input):
        """运行DAG，执行所有节点"""
        sorted_nodes = self.topological_sort()[::-1]
        print(sorted_nodes)
        print(self.nodes,
        self.dependencies)

        if self.config.get('parallel', False):
            # 如果配置为并行执行
            return self.parallel_run_hybrid(sorted_nodes, initial_input)
        else:
            # 如果配置为串行执行
            return self.serial_run(sorted_nodes, initial_input)

    def serial_run(self, sorted_nodes, initial_input):
        """串行执行所有节点"""
        for node_name in sorted_nodes:
            self.data_structure[node_name] = self.execute_node(node_name, initial_input)
        return self.data_structure

    def parallel_run(self, sorted_nodes, initial_input):
        """并行执行所有节点"""
        with ThreadPoolExecutor() as executor:
            futures = {}
            lock = Lock()
            remaining_dependencies = {node: set(deps) for node, deps in self.dependencies.items()}

            def submit_node(node_name):
                future = executor.submit(self.execute_node, node_name, initial_input)
                futures[future] = node_name

            # 提交没有依赖的节点
            for node_name in sorted_nodes:
                if not self.dependencies[node_name]:
                    submit_node(node_name)

            while futures:
                for future in as_completed(futures):
                    node_name = futures.pop(future)
                    try:
                        self.data_structure[node_name] = future.result()
                    except Exception as e:
                        self.nodes[node_name].log(f"An error occurred: {e}", level=logging.ERROR)
                        raise

                    # 提交依赖已经完成的节点
                    with lock:
                        for dependent in self.nodes_depend_on_mapskey[node_name]:
                            remaining_dependencies[dependent].remove(node_name)
                            if not remaining_dependencies[dependent]:
                                submit_node(dependent)

        return self.data_structure

    def parallel_run_hybrid(self, sorted_nodes, initial_input):
        with ThreadPoolExecutor() as thread_executor, ProcessPoolExecutor() as process_executor:
            future_to_node = {}
            lock = Lock()
            remaining_dependencies = {node: set(deps) for node, deps in self.dependencies.items()}

            def submit_node(node_name):
                executor = thread_executor if self.nodes[node_name].impl_type == 'io' else process_executor
                future = executor.submit(self.execute_node, node_name, initial_input)
                future_to_node[future] = node_name

            for node_name in sorted_nodes:
                if not self.dependencies[node_name]:
                    submit_node(node_name)

            while future_to_node:
                for future in as_completed(future_to_node):
                    node_name = future_to_node.pop(future)
                    try:
                        self.data_structure[node_name] = future.result()
                    except Exception as e:
                        self.nodes[node_name].log(f"An error occurred: {e}", level=logging.ERROR)
                        raise

                    with lock:
                        for dependent in self.nodes_depend_on_mapskey[node_name]:
                            remaining_dependencies[dependent].remove(node_name)
                            if not remaining_dependencies[dependent]:
                                submit_node(dependent)

        return self.data_structure
    def print_topological_sort(self):
        sorted_nodes = self.topological_sort()
        print("Topological Sort Order:")
        for node in sorted_nodes:
            print(node)

# 示例JSON配置
config_json = """
{
"parallel": true,
"nodes": [
    {
    "name": "node0",
    "impl": "InputNode"
    },
    {
    "name": "node1",
    "impl": "LengthNode",
    "deps": ["node0"]
    },
    {
    "name": "node2",
    "impl": "FirstCharNode",
    "deps": ["node0"]
    },
    {
    "name": "node3",
    "impl": "ConcatNode",
    "deps": ["node1", "node2"]
    }
]
}
"""

# 加载配置并打印拓扑排序结果
config = json.loads(config_json)
dag = DAG(config)
result = dag.run("Example input data")
print(result)
