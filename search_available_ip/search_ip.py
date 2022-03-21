import os, yaml;
from telnetlib import Telnet;
from ping3 import ping;
from config_log import ConfigLog;

'''实现ping和telnet查看ip是否被占用'''
log = ConfigLog().config_log();


def search(content: dict):
    # 涉及到的端口，22是ssh，3389是windows远程连接，2018和2019是zk端口
    # port_ls = [22, 3389, 2018, 2019];
    port_ls = content.get("check_port");
    ip_net = content.get("check_net");
    ip_range = content.get("check_net_range");
    start = int(ip_range.split("-")[0]);
    end = int(ip_range.split("-")[1]);

    for i in range(start, end + 1):
        # ip = "192.168.200." + str(i);
        ip = ip_net + str(i);
        if ping_connect(ip) is False:
            for j in range(len(port_ls)):
                port = int(port_ls[j]);
                is_connect = telnet_connect(ip, port);
                # 存在true说明连接成功，ip被占用，跳过直接下一个ip
                if is_connect:
                    log.debug(f"{ip}的{port}端口被占用");
                    break;
            else:
                log.info(f"{ip}-->可用");
        else:
            log.debug(f"该{ip}可以ping通,ip被占用");
            continue;


# 使用ping命令查看是否连通，连接成功返回true，失败返回false
def ping_connect(ip: str) -> bool:
    # ping成功返回秒为单位的时间，失败的时候返回的是None
    flag = ping(ip, timeout=1);
    if flag is None:
        return False;
    else:
        return True;


# 连接ip的指定端口，连接成功返回true，失败返回false
def telnet_connect(ip: str, port: int) -> bool:
    tn = Telnet();
    try:
        tn.open(ip, port, 1);
        return True;
    except Exception as e:
        return False;
    finally:
        tn.close();


# 获取yaml文件的内容
def get_yml_data():
    yml_path = "search.yml";
    with open(yml_path, mode="r", encoding="utf-8") as f:
        # 读取yaml的文件内容（dict格式）
        content = yaml.load(f, yaml.FullLoader);
    return content;


if __name__ == '__main__':
    try:
        content = get_yml_data();
        log.info(
            f"正在开始检查ip......{content.get('check_net') + content.get('check_net_range')}:{content.get('check_port')}");
        search(content);
        log.info("所有可用ip检查完毕！")
        os.system("pause");
    except Exception as e:
        log.error(e);
        os.system("pause");
