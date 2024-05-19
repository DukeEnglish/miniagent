from graph.agents.base import AgentBase
from llm_service import glm_client


class ENZHTranslatorAgent(AgentBase):
    def __init__(self, agent_name):
        super().__init__(agent_name)
        self.impl_type = 'io'
    def prompt(self, data):
        tpl = """
            请根据我输入的内容，如果是中文请翻译为英文，如果是英文请翻译为中文。
            输入内容：{data}
                """
        return tpl.format(data=data)
    def process(self, data):
        # 假设data是用户的输入
        res = glm_client.llm(self.prompt(data))
        return res