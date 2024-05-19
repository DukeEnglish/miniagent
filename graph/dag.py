import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from collections import defaultdict
from graph.agents import *
from graph_init import *


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
            if agent_config['impl'] == "FileOutputAgent":
                self.output_agents_list = agent_config["output_agents_list"]
                self.file_path = agent_config["file_path"]

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
        deps_data = [self.env_variable[dep]
                     for dep in self.dependencies[agent_name]]
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
        return output_agent.process(res, self.output_agents_list, self.dependencies[output_agent_name], self.file_path)

    def serial_run(self, sorted_agents, initial_input):
        """串行执行所有节点"""
        for agent_name in sorted_agents:
            self.env_variable[agent_name] = self.execute_agent(
                agent_name, initial_input)
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
            remaining_dependencies = {
                node: set(deps) for node, deps in self.dependencies.items()}

            def submit_node(node_name):
                future = executor.submit(
                    self.execute_node, node_name, initial_input)
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
                        self.nodes[node_name].log(
                            f"An error occurred: {e}", level=logging.ERROR)
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
