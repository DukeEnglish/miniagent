<!--
 * @Descripttion: 
 * @Author: Duke 叶兀
 * @E-mail: ljyduke@gmail.com
 * @Date: 2024-01-03 22:51:03
 * @LastEditors: Junyi_Li ljyduke@gmail.com
 * @LastEditTime: 2024-05-17 18:21:39
-->
# 对话框架 MiniAgent
项目以Node为基础节点，构图运行。

以这个概念作为基础，我们将Node作为Agent，设计一个环境变量env作为Agent的交互变量，用图来组织Agent的运行，从而让所有agents的协作变得清晰简单。


- Node：就是Agent
- 图：就是大的场景设定。预设这个场景下的agent要一起做什么。
- env：就是作用变量，所有的Agent与env进行交互，即环境。

## 1. 构图
整体以Agent为Node，构建图，每个Agent的工作也很明确就是对输入的数据进行某个处理，然后输出即可。

Agent分为三种：Base-Agent、LLM—Agent、Non-LLM-Agent

Base-Agent：基础定义
1. BaseAgent，对Agent的行为做一定约束和统一化管理
2. 接受用户输入，主要是区分string、文件以及文档输入
3. 类似于2，主要做输出处理

LLM-Agent：依赖于大模型的Agent
1. NLU-Agent：输入用户query，输出意图和NER
2. Memory-Agent：输入用户query和NLU结果，提取之前的记忆，包括近几轮对话和
3. Decision-Agent：根据NLU-Agent和Memory-Agent的结果，决策后一步动作：走RAG还是直接给NLG-Agent
4. RAG-Agent：根据NLU-Mem的结果检索知识
5. NLG-Agent：根据环境变量中前序节点生成的结果，构建prompt，由LLM生成
6. Translator-Agent： 翻译Agent

Non-LLM-Agent：不依赖于大模型的Agent，大多数基础的函数计算以及plugin均可以定义在这里
1. 计数
2. 首字母
3. concat
4. 外部API：arxiv、google search api

## 2. 配置与开发共存
所有Agent无法通过图进行直接交互，我们认为他们的交互都是需要介质（env）的，所有需要直接交互的我们认为可以作为一个封装好的Agent存在，这种需要直接进行编码。

通过以上这种操作，我们将所有概念简化并清晰化，寻找到一个复杂与简化的平衡点：将简化的部分留给所有人，并通过清晰的定义将相对复杂的内部结构暴露给开发者。

设计之初，认为所有试图预先定义好一切，封装所有从而让大家全傻瓜式的使用或者完全暴露底层均不是好的设计，都可以做到，保持灵活性才是应该的。
<div style="display: flex; justify-content: center; align-items: center;">
  <img src="https://n.sinaimg.cn/sinacn08/67/w1000h667/20180604/e6a2-hcmurvh2560051.jpg" style="width: 30%; height: 15%;" />
</div>


## 3. 项目思考
参考了市场上的一些agent框架后，发现他们将agent当成人，或者当成某个现实场景映射进行考虑，所以进行了大量的角色预定义。在这个项目中放弃了这个概念，仅引入一个Agent的概念，它的角色和要做的事情完全通过图进行控制，由用户进行相关设计。

这里当我们抛弃了“场景”的预设条件后，此时一个Agent的概念就放大到了整个世界中的任何一个Object，它所充当的角色可以由用户随意定义。换句话说，我现在设计了一份prompt，是要让一个agent可以进行翻译的。

我们将图作为“场景”，将用户的大前提背景作为Prompt，默认构建在每一个agent输入的prompt中，从而让agent知道自己在这个场景下应该扮演的角色，在这里我们实现了Agent的复用。

## Agent商店
作者设计了一些Agent，见；

## 项目布局
本项目是一个框架，其支持基础的底层api交互，同时也提供了一个简单的前端供娱乐玩耍
1. graph：定义基础的图结构，包括节点、边、属性等
2. config：大模型的基础配置
3. main：函数主要入口
4. llm_service：llm服务的调用
5. debug_folder：debug用的
6. dag：图的配置
7. app：前端以及一些资源设置


## 发现与TODO
作者发现，对于很多人来说，所谓的不具备编码能力，本质上是不具备环境配置和制定编程语言编码能力，对大多数人来说，用自然语言描述是一个非常ok的能力。所以本项目支持了两个能力：
1. 可以在前端直接进行json配置，后台自动根据用户输入的json进行图的配置
2. 可以通过自然语言描述的方式生成json，后台根据用户输入的json进行图的配置
### TODO
1. 图的可视化->引入图像自动化生成，完成Agents的自动化构建
2. 如果要多个场景一起存在怎么做呢，作者初步考虑是通过变量传递来实现，此时以服务的概念，构建不同服务之间的调度关系并进行输入输出的重新管理。


**降本增效，就意味着品质的下滑。**

**感谢GLM免费赠送的预算，这在调试过程中十分宝贵**

**本项目的开发中大量依赖了kimi、小部分的gpt3.5/4o，感谢**