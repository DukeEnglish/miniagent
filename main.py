'''
Author: ljyduke 叶兀
Date: 2024-01-03 22:51:43
LastEditors: Duke 叶兀
LastEditTime: 2024-01-08 23:32:00
FilePath: /paper_tutor/main.py
Description: 

Copyright (c) 2024 by ${ljyduke@gmail.com}, All Rights Reserved. 
'''
from graph_init import *
from graph.dag import DAG
import json
# 这里就是读取图配置，并且建立图，然后运行


def load_graph(config_path):
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    return config


def get_dag(dag_config):
    return DAG(dag_config)


def dag_run(dag, initial_input):
    # 创建DAG实例并运行

    try:
        result = dag.run(initial_input)
        logger.info(f"Final Result: {result}")
    except ValueError as e:
        logger.error(e)


def main():
    config_path = "dag_conf/marketing_text_file.conf"
    dag = get_dag(load_graph(config_path))
    initial_input = "给我写十条小红书用的文案"
    dag_run(dag, initial_input)

def main_file():
    config_path = "dag_conf/story_create_file.conf"
    dag = get_dag(load_graph(config_path))
    file_input_path = "/Users/duke/Work/freelife/miniagent/output.txt"
    dag_run(dag, file_input_path)

def main_code():
    """很有用，帮忙读代码
    """
    config_path = "dag_conf/code_reading.conf"
    dag = get_dag(load_graph(config_path))
    file_input_path = "/Users/duke/Work/freelife/miniagent/llm_service"
    dag_run(dag, file_input_path)

def main_coder():
    """很有用，帮忙读代码
    """
    config_path = "dag_conf/coder.conf"
    dag = get_dag(load_graph(config_path))
    dag_run(dag, "帮我写个快速排序")

def main_readme():
    """很有用，帮忙读代码
    """
    config_path = "dag_conf/readme_syn.conf"
    dag = get_dag(load_graph(config_path))
    dag_run(dag, "README_ZH.md")
    
if __name__ == "__main__":
    # main()
    # main_file()
    # main_code()
    # main_coder()
    main_readme()
