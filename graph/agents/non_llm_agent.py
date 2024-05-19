from graph.agents.base import AgentBase

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
