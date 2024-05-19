'''
Author: Junyi_Li ljyduke@gmail.com
Date: 2024-05-15 23:37:18
LastEditors: Junyi_Li ljyduke@gmail.com
LastEditTime: 2024-05-17 00:38:04
FilePath: /Mayfif/Nodebase.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from abc import ABC, abstractmethod
import logging


# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
