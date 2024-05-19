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
    config_path = "dag_conf/story_create.conf"
    dag = get_dag(load_graph(config_path))
    initial_input = "帮我写一个100字的小说"
    dag_run(dag, initial_input)


if __name__ == "__main__":
    main()
