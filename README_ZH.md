<!--
 * @Descripttion: 
 * @Author: Duke 叶兀
 * @E-mail: ljyduke@gmail.com
 * @Date: 2024-01-03 22:51:03
 * @LastEditors: Junyi_Li ljyduke@gmail.com
 * @LastEditTime: 2024-05-19 20:05:55
-->
# 对话框架 miniagent

项目地址：https://github.com/DukeEnglish/miniagent

# 项目介绍

当前已经有很多对话机器人制作平台出现了，很好用，不过他们也有缺点，比如日志不开放，封装过于完备，开发者自由度过低等。

同样的，也有很多框架在github上，很流行也很强大。不过越强大，自然也就会封装越严密。

所以这里就以一个很普通的视角来进行开发，参考上述各种强大的框架的功能进行设计，做一个小而美的框架。

1. 多种大模型接入方式，快速方便，隐私安全，可以一键运行
2. 支持文件/文件夹输入/输出方式，快速理解生产大批量内容，小说文案快速生产
3. 项目信奉广义Agent，所以以Agent为Node构建图，支持LLM-agent与non-LLM-agent
4. 项目支持配置化进行，提供多种基础Agent，方便构图并进行使用
5. 项目支持简单的前端与API接入，方便展示也方便与各个模块进行集成
6. [todo] 提供了对日志的管理和处理模块，对于使用者来说可以方便基于自己的使用习惯保留数据，为后续模型/prompt优化使用
7. [todo] 多参数输入，以字典形式输入，这样可以对不同的node输入参数，这里主要是针对basenode的一些灵活输入，其他的均可以直接在图中配置
8. [todo] 增加部分全局配置，适配更多不同模型使用
9. 【todo】在任务型场景下，怎么在这个基础上完成交互型场景

## 示例任务
所有的预设图均在dag_conf中。

- story_create.conf: 让大模型帮助持续的写小说，而不用自己手动一个个交互，将其配置在main函数的路径中即可看到结果。
- code_reading.conf: 让大模型帮助读代码，可以输入文件/文件夹直接读，很爽，节约时间利器
- coder.conf: 让大模型帮忙写代码

## 支持

如果您喜欢这个项目，请给一个星标 🌟 以示支持！感谢～


## 欢迎进群交流，后续新的项目更新会在群里
<div style="display: flex;">
  <img src="https://github.com/DukeEnglish/papertutor/blob/main/assets/qr_code.jpg" style="width: 30%; height: 15%;" />
  <img src="https://github.com/DukeEnglish/papertutor/blob/main/assets/per_qr_code.jpg" style="width: 30%; height: 15%;" />
</div>

## 详细介绍
其他信息见：https://www.zhihu.com/people/ljyduke
