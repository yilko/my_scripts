import logging.config;
import os
import yaml;


# 定义单例模式装饰器函数
# cls指的是类(把类作为参数传进singleton方法)
def singleton(cls):
    _instance = {};

    # get_instance方法参数传的是类实例时的__init__方法参数
    def get_instance(*args, **kwargs):
        if cls not in _instance:
            # key是类，value是类的实例
            _instance[cls] = cls(*args, **kwargs);
        return _instance[cls];

    return get_instance;


@singleton
class ConfigLog:
    def config_log(self,logger_name="my_logger"):
        try:
            # yml_path = os.path.dirname(os.path.abspath(__file__)) + os.path.sep +"config_log.yml";
            yml_path = "config_log.yml";
            with open(file=yml_path, mode='r', encoding="utf-8") as file:
                logging_yaml = yaml.load(stream=file, Loader=yaml.FullLoader)
                # 配置logging日志：主要从文件中读取handler、formatter、logger的配置
                logging.config.dictConfig(config=logging_yaml)
            return logging.getLogger(logger_name);
        except Exception as e:
            print(e);
            os.system("pause");


# if __name__ == '__main__':
#     log = ConfigLog().config_log();
#     log.info("info");
#     log.debug("debug");
#     log.warning("warn")
    # root_log.info("info");
    # root_log.debug("debug");
    # root_log.warning("warn")
