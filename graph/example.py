'''
Author: Junyi_Li ljyduke@gmail.com
Date: 2024-05-15 23:39:12
LastEditors: Junyi_Li ljyduke@gmail.com
LastEditTime: 2024-05-17 00:14:08
FilePath: /Mayfif/function_node/example.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from graph.agents.base import NodeBase
# 定义LengthNode类，继承自NodeBase

class LengthNode(NodeBase):
    def process(self, data):
        """处理逻辑：返回字符串长度"""
        if not isinstance(data, str):
            self.raise_error("Input must be a string")
        return len(data)

# 定义FirstCharNode类
class FirstCharNode(NodeBase):
    def process(self, data):
        """处理逻辑：返回字符串的第一个字符"""
        if not data:
            self.raise_error("Input must not be empty")
        return data[0]

# 定义ConcatNode类
class ConcatNode(NodeBase):
    def process(self, data):
        """处理逻辑：组合长度和第一个字符信息"""
        length, first_char = data
        return f"Length: {length}, First Char: {first_char}"