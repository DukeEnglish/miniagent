<!--
 * @Descripttion: 
 * @Author: Duke 叶兀
 * @E-mail: ljyduke@gmail.com
 * @Date: 2024-01-03 22:51:03
 * @LastEditors: Junyi_Li ljyduke@gmail.com
 * @LastEditTime: 2024-05-19 20:05:55
-->
# 对话框架 TinyAgent

项目地址：https://dukeenglish.github.io/

# 项目介绍

当前已经有很多对话机器人制作平台出现了，很好用，不过他们也有缺点，比如日志不开放，封装过于完备，开发者自由度过低等。

同样的，也有很多框架在github上，很流行也很强大。不过越强大，自然也就会封装越严密。

所以这里就以一个很普通的视角来进行开发，参考上述各种强大的框架的功能进行设计，做一个小而美的框架。
1. 着重提供了对日志的管理和处理模块，对于使用者来说可以方便基于自己的使用习惯保留数据，为后续模型/prompt优化使用
2. 项目信奉广义Agent，所以以Agent为Node构建图，支持LLM-agent与non-LLM-agent
3. 项目支持配置化进行，提供多种基础Agent，方便构图并进行使用
4. 项目支持简单的前端与API接入，方便展示也方便与各个模块进行集成
5. 针对LLM接入，项目支持API，也支持本地部署，方便大家自行调用
6. 为了部分大模型的语言支持问题，我们直接提供了一个中英切换node，可以用来在输入和输出上做切换，帮助用户直接无痛使用自己和模型擅长的语言

姐妹项目：本地部署大模型，简单快速不要钱，POC不是梦 --- TinyAssistant

## 示例任务
在example_graph中

例如，让大模型帮助持续的写小说，而不用自己手动一个个交互，不断运行stroy_graph，即可看到结果

## 支持

如果您喜欢这个项目，请给一个星标 🌟 以示支持！感谢～


## 欢迎进群交流，后续新的项目更新会在群里
<div style="display: flex;">
  <img src="https://github.com/DukeEnglish/papertutor/blob/main/assets/qr_code.jpg" style="width: 30%; height: 15%;" />
  <img src="https://github.com/DukeEnglish/papertutor/blob/main/assets/per_qr_code.jpg" style="width: 30%; height: 15%;" />
</div>

## 详细介绍
其他信息见：https://www.zhihu.com/people/ljyduke