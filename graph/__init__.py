'''
Author: Junyi_Li ljyduke@gmail.com
Date: 2024-05-16 00:26:49
LastEditors: Junyi_Li ljyduke@gmail.com
LastEditTime: 2024-05-17 00:41:01
FilePath: /Mayfif/function_node/__init__.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from graph.example import FirstCharNode, ConcatNode, LengthNode
from graph.base import InputNode

__all__ = [
    'InputNode',
    'FirstCharNode',
    'ConcatNode',
    'LengthNode'
]