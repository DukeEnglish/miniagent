import logging
from abc import ABC, abstractmethod
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from collections import defaultdict
from llm_service import glm_client
# 配置日志记录
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# 定义抽象基类AgentBase
class AgentBase(ABC):
    def __init__(self, agent_name):
        self.agent_name = agent_name
        self.impl_type = 'io'

    def log(self, message, level=logging.INFO):
        """记录日志信息"""
        class_name = self.__class__.__name__
        prefix = f"[{class_name}::{self.agent_name}] "
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

class ENZHTranslatorAgent(AgentBase):
    def __init__(self, agent_name):
        super().__init__(agent_name)
        self.impl_type = 'io'
    def prompt(self, data):
        tpl = """
            请根据我输入的内容，如果是中文请翻译为英文，如果是英文请翻译为中文。
            输入内容：{data}
                """
        return tpl.format(data=data)
    def process(self, data):
        # 假设data是用户的输入
        res = glm_client.llm(self.prompt(data))
        return res

class FolderInputAgent(AgentBase):
    def __init__(self, agent_name):
        super().__init__(agent_name)
        self.impl_type = 'io'
    def process(self, folder_path):
        # 初始化一个空字符串用于存储所有文件内容
        file_contents = ""
        # 遍历文件夹中的所有文件
        for filename in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, filename)):
                with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                    file_contents += file.read() + "\n"  # 读取文件内容并添加换行符
        return file_contents
    
class FileInputAgent(AgentBase):
    def __init__(self, agent_name):
        super().__init__(agent_name)
        self.impl_type = 'io'
    def process(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

# 输入节点，从用户获取输入数据
class InputAgent(AgentBase):
    def __init__(self, agent_name):
        super().__init__(agent_name)
        self.impl_type = 'io'
    def process(self, data):
        # 假设data是用户的输入
        return data

class OutputAgent(AgentBase):
    def __init__(self, agent_name):
        super().__init__(agent_name)

    def process(self, env, agents):
        # 如果需要返回所有代理的输出结果
        if not agents:
            return env
        # 如果只需要返回特定代理的输出结果
        else:
            # 假设 agents 是一个包含代理名称的列表
            
            return {agent_name: env.get(agent_name) for agent_name in agents if agent_name in agents}
        
# 计算输入数据长度的节点
class LengthAgent(AgentBase):
    def __init__(self, agent_name):
        super().__init__(agent_name)
        self.impl_type = 'io'
    def process(self, data):
        return len(data[0])

# 获取输入数据第一个字符的节点
class FirstCharAgent(AgentBase):
    def __init__(self, agent_name):
        super().__init__(agent_name)
        self.impl_type = 'io'
    def process(self, data):
        return data[0][0] if data else None

# 将多个依赖节点的数据连接起来的节点
class ConcatAgent(AgentBase):

    def process(self, data):
        out = ""
        for i in data:
            out += str(i) if i else ""
        return out

# 定义DAG类，用于解析JSON配置和执行节点
class DAG:
    def __init__(self, config):
        self.config = config
        self.agents = {}
        self.dependencies = {}
        self.env_variable = {}
        self.output_agents_list = []
        self.nodes_depend_on_mapskey = defaultdict(list)
        self.load_agents()

    def load_agents(self):
        """加载节点配置，实例化节点对象"""
        for agent_config in self.config['agents']:
            name = agent_config['name']
            impl = globals()[agent_config['impl']]
            agent = impl(name)
            self.agents[name] = agent
            self.dependencies[name] = agent_config.get('deps', [])
            for dep in self.dependencies[name]:
                self.nodes_depend_on_mapskey[dep].append(name)
            if agent_config['impl'] == "OutputAgent":
                self.output_agents_list = agent_config["output_agents_list"]

    def topological_sort(self):
        """拓扑排序，确保节点按依赖顺序执行"""
        indegree = {agent: 0 for agent in self.agents}
        for deps in self.dependencies.values():
            for dep in deps:
                indegree[dep] += 1

        queue = [agent for agent in self.agents if indegree[agent] == 0]
        sorted_agents = []

        while queue:
            agent = queue.pop(0)
            sorted_agents.append(agent)
            for dep in self.dependencies[agent]:
                indegree[dep] -= 1
                if indegree[dep] == 0:
                    queue.append(dep)

        if len(sorted_agents) != len(self.agents):
            raise ValueError("Graph has cycles")

        return sorted_agents
    
    def execute_agent(self, agent_name, initial_input):
        
        agent = self.agents[agent_name]
        deps_data = [self.env_variable[dep] for dep in self.dependencies[agent_name]]
        return agent.run(deps_data if deps_data else initial_input)

    def run(self, initial_input):
        """运行DAG，执行所有节点"""
        sorted_agents = self.topological_sort()[::-1]
        # 从sorted_agents中移除OutputAgent并保存到单独的变量中
        output_agent_name = 'output_agent'
        sorted_agents.remove(output_agent_name)
        output_agent = self.agents[output_agent_name]

        if self.config.get('parallel', False):
            # 如果配置为并行执行
            res = self.parallel_run(sorted_agents, initial_input)
        else:
            # 如果配置为串行执行
            res = self.serial_run(sorted_agents, initial_input)
        return output_agent.process(res, self.output_agents_list)

    def serial_run(self, sorted_agents, initial_input):
        """串行执行所有节点"""
        for agent_name in sorted_agents:
            self.env_variable[agent_name] = self.execute_agent(agent_name, initial_input)
        return self.env_variable

    def parallel_run(self, initial_input):
        self.env_variable = {}
        execution_order = self.topological_sort()
        futures = {}
        with ThreadPoolExecutor() as executor:
            for agent_name in execution_order:
                if self.agents[agent_name].impl_type == 'io':
                    future = executor.submit(self.execute_agent, agent_name)
                else:
                    future = executor.submit(self.execute_agent, agent_name)
                futures[agent_name] = future
        for agent_name, future in as_completed(futures.values()):
            self.env_variable[agent_name] = future.result()
        return self.env_variable
    
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

        return self.env_variable
    
    def print_topological_sort(self):
        sorted_agents = self.topological_sort()
        print("Topological Sort Order:")
        for agent in sorted_agents:
            print(agent)

if __name__ == "__main__":

    # 示例JSON配置
    config_json = """
    {
    "parallel": false,
    "agents": [
        {
        "name": "input_agent",
        "impl": "InputAgent"
        },
        {
        "name": "agent1",
        "impl": "LengthAgent",
        "deps": ["input_agent"]
        },
        {
        "name": "agent2",
        "impl": "FirstCharAgent",
        "deps": ["input_agent"]
        },
        {
        "name": "agent3",
        "impl": "ConcatAgent",
        "deps": ["agent1", "agent2"]
        },
        {
        "name": "output_agent",
        "impl": "OutputAgent",
        "deps": ["agent3"],
        "output_agents_list": ["agent3"]
        }
    ]
    }
    """
    # 加载配置并打印拓扑排序结果
    config = json.loads(config_json)
    dag = DAG(config)
    dag.print_topological_sort()
    result = dag.run("Example input data")
    print(result)
