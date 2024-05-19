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
            输入内容：{data}
                """
        return tpl.format(data=data)


class StoryAgent(LLMAgent):
    def prompt(self, data):
        tpl = """
            请根据我输入的内容，完成任务。
            输入内容：{data}
                """
        return tpl.format(data=data)

