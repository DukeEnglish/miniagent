import ast
from collections import defaultdict
import networkx as nx
from graph.agents.base import AgentBase
import logging
from abc import ABC, abstractmethod
import os
import requests

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

class PromptConstructAgent(AgentBase):

    def process(self, data):
        data = f"""
            请后续的对话在给定信息的基础上进行讨论。
            首先请给出这个项目的主要简介{data}
        """
        
        return data



class CodeInputAgent(AgentBase):
    def __init__(self, agent_name, input_type, input_value):
        super().__init__(agent_name)
        self.input_type = input_type  # 'file', 'folder', 或 'github-repo'
        self.input_value = input_value  # 输入的具体值，例如文件路径或GitHub仓库URL

    def process(self, data):
        """具体处理逻辑，根据输入类型读取数据"""
        if self.input_type == 'file':
            return self._process_file(data)
        elif self.input_type == 'folder':
            return self._process_folder(data)
        elif self.input_type == 'github-repo':
            return self._process_github_repo(data)
        else:
            self.raise_error("Unsupported input type")

    def _process_file(self, file_path):
        """处理单个文件"""
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except IOError as e:
            self.raise_error(f"Failed to read file {file_path}: {e}")

    def _process_folder(self, folder_path):
        """处理文件夹，返回文件夹中所有文件的内容列表"""
        try:
            files_content = []
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    with open(file_path, 'r') as file:
                        files_content.append(file.read())
            return files_content
        except IOError as e:
            self.raise_error(f"Failed to process folder {folder_path}: {e}")

    def _process_github_repo(self, repo_url):
        """处理GitHub仓库，返回仓库中的文件内容"""
        try:
            # 这里只是一个示例，实际的GitHub API调用会更复杂
            response = requests.get(repo_url)
            response.raise_for_status()
            # 假设响应是JSON格式，包含文件列表和内容
            files_content = [(file['name'], file['content'])
                             for file in response.json()]
            return files_content
        except requests.RequestException as e:
            self.raise_error(f"Failed to access GitHub repo {repo_url}: {e}")


class ProjectAnalyzer(ast.NodeVisitor):
    """这个类具备的功能：
    1. 做到ast分析
    2. 调用图和控制流图

    Args:
        ast (_type_): _description_
    """

    def __init__(self):
        self.project_structure = defaultdict(
            lambda: {'classes': [], 'functions': [], 'imports': set()})
        self.function_defs = {}  # 存储函数定义的映射
        self.current_function = None
        self.current_class = None
        self.cfg = nx.DiGraph()  # 控制流图
        self.cdg = nx.DiGraph()  # 调用图

    def add_cfg_edge(self, src, dst):
        self.cfg.add_edge(f'"{src}"', f'"{dst}"')

    def add_cdg_edge(self, caller, callee):
        self.cdg.add_edge(f'"{caller}"', f'"{callee}"')

    def get_function_key(self, node):
        return f"{self.current_class or ''}:{node.name}".replace(':', '\":')

    def visit_FunctionDef(self, node):
        prev_function = self.current_function
        self.current_function = self.get_function_key(node)
        self.function_defs[self.current_function] = node
        self.project_structure[self.current_file]['functions'].append({
            'name': node.name,
            'lineno': node.lineno,
            'docstring': self.get_docstring(node)
        })
        self.generic_visit(node)
        self.current_function = prev_function

    def visit_ClassDef(self, node):
        prev_class = self.current_class
        self.current_class = node.name
        self.project_structure[self.current_file]['classes'].append({
            'name': node.name,
            'lineno': node.lineno,
            'docstring': self.get_docstring(node)
        })
        self.generic_visit(node)
        self.current_class = prev_class

    def visit_Import(self, node):
        for alias in node.names:
            self.project_structure[self.current_file]['imports'].add(
                alias.name)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            if alias.asname:
                import_name = alias.asname
            else:
                import_name = alias.name
            self.project_structure[self.current_file]['imports'].add(
                (node.module, import_name))

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and self.current_function:
            caller = self.current_function
            callee = node.func.id
            self.add_cdg_edge(caller, callee)

    def visit_If(self, node):
        self.add_cfg_edge(f"BeforeIf:{node.lineno}", f"IfStart:{node.lineno}")
        self.generic_visit(node)
        self.add_cfg_edge(f"IfEnd:{node.lineno}", f"AfterIf:{node.lineno}")

    # 需要为其他AST节点添加visit_*方法，并相应地更新CFG

    def get_docstring(self, node):
        return ast.get_docstring(node) if node.body else None

    def visualize_graph(self, G, filename):
        # 使用pydot转换networkx图
        P = nx.drawing.nx_pydot.to_pydot(G)

        # 确保所有节点名称和属性被正确引用
        for node in P.get_node_list():
            node.set_name(node.get_name().replace(':', '\":'))

        # 将pydot图转换为dot脚本并保存为图像文件
        dot_script = P.to_string()
        with open(filename, 'w') as f:
            f.write(dot_script)

        # 使用Graphviz的dot命令生成图像文件
        os.system(f"dot -Tpng {filename} -o {filename.split('.')[0]}.png")

    def analyze_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            tree = ast.parse(content, filename=file_path)
            self.current_file = file_path
            self.visit(tree)

    def generate_directory_tree(self, directory, ignore_dirs=None):
        if ignore_dirs is None:
            ignore_dirs = {".git", ".venv",
                           "node_modules", "__pycache__", ".DS_Store"}

        tree = {}
        for root, dirs, files in os.walk(directory):
            # 检查目录是否在忽略列表中
            for d in dirs:
                if d in ignore_dirs:
                    dirs.remove(d)  # 从当前遍历的目录中移除

            relative_path = os.path.relpath(root, directory)
            tree[relative_path] = {
                'dirs': list(dirs),
                'files': list(files)
            }
        return tree

    def print_directory_tree(self, tree, md_file):
        """
        打印目录树结构。

        Args:
            tree (dict): 目录树数据结构。
            indent (int): 当前缩进级别。
        """
        md_file.write(f"## 项目目录结构如下：\n")
        for name, content in tree.items():
            md_file.write(f"{name}/\n")
            for dir_name in content['dirs']:
                md_file.write(f"    - {dir_name}/\n")
            for file_name in content['files']:
                md_file.write(f"    - {file_name}\n")

    def analyze_project(self, directory, md_file):
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    self.analyze_file(file_path)
        md_file.write("\n## Project Structure\n")
        for file, contents in self.project_structure.items():
            md_file.write(f"### {os.path.relpath(file, directory)}\n")
            for item_type, items in contents.items():
                md_file.write(f"#### {item_type.capitalize()}:\n")
                for item in items:
                    if isinstance(item, dict):
                        md_file.write(
                            f"- **{item['name']}** at line {item['lineno']} - Docstring: {item.get('docstring', 'No docstring')}\n")

        # 写入CFG和CDG节点信息到Markdown文件
        md_file.write("\n## Graphs\n")
        md_file.write(f"### CFG Nodes: {list(self.cfg.nodes)}\n")
        md_file.write(f"### CDG Nodes: {list(self.cdg.nodes)}\n")


# 使用示例
if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # 创建CodeInputAgent实例
    agent = CodeInputAgent(agent_name="CodeInputAgent",
                           input_type="file", input_value="/path/to/your/file")

    # 运行agent处理逻辑
    try:
        data = agent.run("some data if needed")
        print(data)
    except Exception as e:
        print(f"An error occurred: {e}")

    def main():
        # 使用示例
        project_directory = './'  # 替换为你的项目文件夹路径
        project_md_file = 'project_structure.md'  # Markdown文件名
        analyzer = ProjectAnalyzer()
        analyzer = ProjectAnalyzer()
        directory_tree = analyzer.generate_directory_tree(project_directory)
        with open(project_md_file, 'w', encoding='utf-8') as md_file:
            md_file.write(f"# 项目解析信息如下：\n")
            analyzer.print_directory_tree(directory_tree, md_file)
            analyzer.analyze_project(project_directory, md_file)

        # 可视化CFG和CDG
        analyzer.visualize_graph(analyzer.cfg, 'cfg.dot')
        analyzer.visualize_graph(analyzer.cdg, 'cdg.dot')
