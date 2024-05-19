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


def dag_run(dag_config):
    # 创建DAG实例并运行
    dag = DAG(dag_config)
    try:
        result = dag.run("你好啊")
        logger.info(f"Final Result: {result}")
    except ValueError as e:
        logger.error(e)


def main():
    config_path = "dag_conf/example.conf"
    dag_run(load_graph(config_path))


if __name__ == "__main__":
    main()
