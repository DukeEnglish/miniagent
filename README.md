<!--
 * @Description: 
 * @Author: Duke 叶兀
 * @E-mail: ljyduke@gmail.com
 * @Date: 2024-01-03 22:51:03
 * @LastEditors: Junyi_Li ljyduke@gmail.com
 * @LastEditTime: 2024-05-19 20:05:55
-->
# Dialogue Framework miniagent

Project Link: https://github.com/DukeEnglish/miniagent

# Project Introduction

There are already many dialogue robot production platforms available, which are very useful, but they also have shortcomings, such as closed logs, overly complete encapsulation, and low developer freedom.

Similarly, there are also many frameworks on GitHub, which are very popular and powerful. However, the more powerful they are, the more tightly encapsulated they will naturally be.

Therefore, here we will develop from a very ordinary perspective, referring to the functions of various powerful frameworks mentioned above to design a small and beautiful framework.

1. Multiple ways to access large models, fast and convenient, privacy-safe, and can be run with one click
2. Supports file/folder input/output methods, quickly understands the production of large quantities of content, and quickly produces novel copies
3. The project believes in a broad sense of Agent, so it constructs a graph with Agent as Node, supporting both LLM-agent and non-LLM-agent
4. The project supports configuration-based operation, providing a variety of basic Agents for easy graph construction and use
5. The project supports simple front-end and API access, making it easy to display and integrate with various modules
6. [todo] Provides a log management and processing module, which makes it convenient for users to retain data based on their usage habits, for subsequent model/prompt optimization
7. [todo] Multiple parameter input, in the form of a dictionary input, so that different node input parameters can be specified. This is mainly for some flexible inputs of basenode, and others can be directly configured in the graph
8. [todo] Add some global configurations to adapt to the use of more different models

## Sample Tasks
All preset graphs are in dag_conf.

- story_create.conf: Let the large model continue to write novels without manually interacting one by one, and configure it in the main function path to see the results.
- code_reading.conf: Let the large model help read code, can directly read files/folders, very cool, a time-saving tool
- coder.conf: Let the large model help write code

## Support

If you like this project, please give it a star 🌟 to show your support! Thank you～

## Welcome to join the group for communication. New project updates will be in the group
<div style="display: flex;">
  <img src="https://github.com/DukeEnglish/papertutor/blob/main/assets/qr_code.jpg" style="width: 30%; height: 15%;" />
  <img src="https://github.com/DukeEnglish/papertutor/blob/main/assets/per_qr_code.jpg" style="width: 30%; height: 15%;" />
</div>

## Detailed Introduction
For other information, see: https://www.zhihu.com/people/ljyduke