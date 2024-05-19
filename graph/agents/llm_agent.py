from graph.agents.base import AgentBase
from llm_service import glm_client
from abc import ABC, abstractmethod

class LLMAgent(AgentBase):
    def __init__(self, agent_name):
        super().__init__(agent_name)
        self.impl_type = 'io'

    @abstractmethod
    def prompt(self, data):
        pass
    
    def process(self, data):
        # data是用户的输入
        res = glm_client.llm(self.prompt(data))
        return res

    
class ENZHTranslatorAgent(LLMAgent):
    def prompt(self, data):
        tpl = """
            请根据我输入的内容，如果是中文请翻译为英文，如果是英文请翻译为中文。
            1. 格式保持原样
            2. 仅输出翻译后的结果，不要擅自增加东西
            输入内容：{data}
                """
        return tpl.format(data=data)


class StoryAgent(LLMAgent):
    def prompt(self, data):
        tpl = """
            请根据我输入的内容，将小说继续写下去
            输入内容：{data}
                """
        return tpl.format(data=data)

class CodeReaderAgent(LLMAgent):
    def prompt(self, data):
        tpl = """
            请根据我输入的内容，将代码分析清楚，最终用markdown的格式帮我把代码讲解清楚
            输入内容：{data}
                """
        return tpl.format(data=data)

class CoderAgent(LLMAgent):
    def prompt(self, data):
        tpl = """
            根据我输入的内容，帮我完成要完成的代码任务
            输入内容：{data}
                """
        return tpl.format(data=data)
