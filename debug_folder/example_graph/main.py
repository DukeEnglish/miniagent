from graph.agents import *
import json

if __name__ == "__main__":

    # 示例JSON配置
    config_json = """
    {
    "parallel": false,
    "agents": [
        {
        "name": "input_agent",
        "impl": "InputAgent"
        },
        {
        "name": "agent1",
        "impl": "LengthAgent",
        "deps": ["input_agent"]
        },
        {
        "name": "agent2",
        "impl": "FirstCharAgent",
        "deps": ["input_agent"]
        },
        {
        "name": "agent3",
        "impl": "ConcatAgent",
        "deps": ["agent1", "agent2"]
        },
        {
        "name": "output_agent",
        "impl": "OutputAgent",
        "deps": ["agent3"],
        "output_agents_list": ["agent3"]
        }
    ]
    }
    """
    # 加载配置并打印拓扑排序结果
    config = json.loads(config_json)
    dag = DAG(config)
    dag.print_topological_sort()
    result = dag.run("Example input data")
    print(result)
