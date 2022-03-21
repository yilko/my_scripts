import logging;
import sys;
'''
python代码方式配置log
'''

# 不写默认是root logger,有名字的话给logger命名
# __name__指模块下的名字(xxx.xxx.xxx), __file__指该py文件的绝对路径(D:\xxx\xxx\xxx.py)
log = logging.getLogger(__name__);
# 给logger设置日志级别
log.setLevel(logging.INFO);
# 添加流处理器和文件处理器并设置日志级别
# 流处理器默认使用sys.stderr
# sys.stdin(标准输入),sys.stdout(标准输出[print语句使用的是这个]),sys.stderr(错误输出)
stream_handler = logging.StreamHandler(sys.stdout);
stream_handler.setLevel(logging.INFO);
# 创建一个文件处理器并指定文件名(暂不知道是否支持路径)
file_handle = logging.FileHandler("log.txt");
# 输入到文件的日志级别提高
file_handle.setLevel(logging.WARNING);
# 添加格式器
format_str = "%(asctime)s - %(filename)s - [line:%(lineno)d] - %(levelname)s: %(message)s";
formatter = logging.Formatter(format_str);
# 处理器添加格式器
stream_handler.setFormatter(formatter);
file_handle.setFormatter(formatter);
# 日志器添加处理器
log.addHandler(stream_handler);
log.addHandler(file_handle);


if __name__ == '__main__':
    log.info("aaaaaaa");
    log.warning("bbbbbbb");