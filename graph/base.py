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

class NodeBase(ABC):
    def __init__(self, node_name):
        self.node_name = node_name
        self.data_structure = {}

    def log(self, message, level=logging.INFO):
        """记录日志信息"""
        class_name = self.__class__.__name__
        prefix = f"[{class_name}::{self.node_name}] "
        logger.log(level, prefix + message)#, )

    def raise_error(self, message):
        """统一构建异常信息并引发错误"""
        self.log(message, level=logging.ERROR)
        raise ValueError(message)

    @abstractmethod
    def process(self, data):
        pass

    def run(self, data):
        """运行节点的process方法，并记录输入输出"""
        try:
            self.log(f"Processing input data: {data}")
            result = self.process(data)
            self.log(f"Output data: {result}")
            self.data_structure[self.node_name] = result
        except Exception as e:
            self.log(f"An error occurred: {e}", level=logging.ERROR)
            raise

# 输入节点，用于初始化数据流
class InputNode(NodeBase):
    def process(self, data):
        """输入节点不执行任何处理，直接返回数据"""
        return data
