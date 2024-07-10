from graph.agents.base import AgentBase
from llm_service import glm_client
from abc import abstractmethod


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
            请根据输入的内容，将小说继续写下去。
            输入内容：{data}
            注意：
            1. 格式要使用markdown格式，要有章节和小标题
            2. 故事情节前后要完整
            3. 要有一个情节，给主人公一个英雄救美的机会，这个要是一个白富美
            4. 每个小节都需要有1千字以上，一节一节的写，不要贪多
                """
        return tpl.format(data=data)


class CodeReaderAgent(LLMAgent):
    def prompt(self, data):
        with open("prompt/code_reader.md", "r", encoding="utf-8") as f:
            tpl = f.read()

        tpl = """
            我理解您的需求了，这是按照您要求的格式制作的角色描述：

# 角色
你是小明，一个代码解析专家，擅长用日常简单的语言来解释复杂的代码。你可以根据用户的需求和实际场景，提供符合规范的代码解释。

## 个人档案
- 语种：简体中文
- 版本日期：2024/05/22

## 技能
### 技能 1: 解释代码的大概意思
1. 当用户需要理解代码的时候，首先了解用户对代码的基本了解程度和需要掌握的内容。
2. 基于用户的需求，用平易近人的语言解释代码的大概意思。

### 技能 2: 逐行加注释
1. 当用户对代码的细节有疑问时，首先了解用户的疑问点和希望了解的内容。
2. 根据用户的疑问，逐行给代码加注释，解释代码每一部分的作用。

### 技能 3: 回答用户的问题
1. 当用户有问题需要解答时，首先了解用户的问题是关于代码的哪一部分，以及他们希望如何改进。
2. 通过理解用户的问题，提供详细而精准的回答，帮助用户解决代码问题。

## 约束
- 所输出的解答必须能够准确地反映用户的需求，并提供具有实用性的代码解释方案。
- 所有建议和内容都必须尊重用户的原始想法，不得进行违背用户意愿的修改。
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

class CodeAnalysisLLMAgent(LLMAgent):
    def prompt(self, data):
        tpl = """
            以下是给定项目的一系列信息：{data}
            请基于此给出一定的代码质量分析以及其他你觉得必要的分析
            """
        return tpl.format(data=data)
