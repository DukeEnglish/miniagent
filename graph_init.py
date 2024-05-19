import logging
import importlib

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 配置项目基础配置
module_name = "graph"
module = importlib.import_module(module_name)

