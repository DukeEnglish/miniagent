from abc import ABC, abstractmethod
import logging
import networkx as nx
import matplotlib.pyplot as plt
from graph.example import FirstCharNode, ConcatNode, LengthNode
import json
from pathlib import Path
import importlib.util
from typing import List, Any, Callable
# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
module_name = "graph"
module = importlib.import_module(module_name)


def dynamic_import_and_create_instance(class_name):
    try:
        # 通过模块获取指定的类
        cls = getattr(module, class_name)
        return cls
    except ImportError as e:
        print(f"Error importing module '{module_name}': {e}")
        return None
    except AttributeError as e:
        print(f"Class '{class_name}' not found in module '{module_name}': {e}")
        return None


class DAG:
    def __init__(self, config):
        self.config = config
        self.nodes = {}
        self.edges = {}

        # 创建节点实例并初始化nodes和edges字典
        for node_config in config['nodes']:
            node_name = node_config['name']
            self.nodes[node_name] = dynamic_import_and_create_instance(
                node_config["impl"])(node_config['name'])
            if 'deps' in node_config:
                self.edges[node_name] = node_config['deps']
    #     return initial_data

    def run(self, initial_data):
        # ""“按拓扑排序的顺序运行DAG中的节点”""
        execution_order = self.topological_sort()
        current_data = initial_data
        results = {}

        for node_name in execution_order:
            node = self.nodes[node_name]
            node.data_structure[node.node_name]

            result = node.run(current_data)
            results[node_name] = result
            current_data = result

        return results

    def add_node(self, node):
        self.nodes[node.node_name] = node
        self.execution_order.append(node)

    def add_edge(self, from_node_name, to_node_name):
        # 这里需要实现依赖关系的具体逻辑
        pass

    def topological_sort(self):
        visited = set()
        sort_order = []

        def dfs(node):
            if node in visited:
                return
            visited.add(node)
            for dep in self.edges.get(node, []):
                dfs(dep)
            sort_order.append(node)

        for node in self.nodes:
            if node not in visited:
                dfs(node)
        return sort_order

    def visualize(self):
        G = nx.DiGraph()
        for node in self.nodes.values():
            G.add_node(node.name)
        for source, targets in self.edges.items():
            for target in targets:
                G.add_edge(source, target)
        nx.draw(G, with_labels=True, arrows=True)
        plt.show()


if __name__ == '__main__':
    import json
    # JSON配置
    dag_config = """
    {
    "nodes": [
        {
        "name": "node0",
        "impl": "InputNode"
        "type": "io"
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

    # 解析JSON配置
    dag_json = json.loads(dag_config)

    # 创建DAG实例并运行
    dag = DAG(dag_json)
    dag.visualize()
    try:
        result = dag.run("sdfsd")
        logger.info(f"Final Result: {result['node3']}")
    except ValueError as e:
        logger.error(e)
