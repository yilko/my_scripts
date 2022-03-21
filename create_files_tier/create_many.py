import os, yaml, time;
from create_files_tier.config_log import ConfigLog;
'''实现本地递归创建文件夹和txt文件'''

log = ConfigLog().config_log();


# 创建文件夹
def create_folder(content: dict):
    path = content.get("root_path");
    two_tier_folder_nums = content.get("two_tier_folder_nums");
    tier_nums = content.get("tier_nums");
    log.info("正在创建文件夹....");
    for i in range(two_tier_folder_nums):
        folder_path2 = f"{path}/2tier_{i}";
        folder_exist = os.path.exists(folder_path2);
        if not folder_exist:
            os.mkdir(folder_path2);
        # 前面已有两层，从第三层开始
        for i in range(3, tier_nums + 1):
            folder_path2 += f"/{i}tier";
            os.mkdir(folder_path2);
    log.info("所有文件夹创建完毕！准备创建文件....")


# 创建文件
def create(content: dict):
    path = content.get("root_path");
    file_nums = int(content.get("file_nums"));
    two_tier_folder_nums = int(content.get("two_tier_folder_nums"));
    tier_nums = int(content.get("tier_nums"));
    txt_content = str(content.get("txt_content"));
    if file_nums > 0:
        folder_nums = (tier_nums - 1) * two_tier_folder_nums;
        file_num_each_folder = file_nums // folder_nums;
        log.info(f"总共有{file_nums}个文件，总共有{folder_nums}个文件夹，每个文件夹存{file_num_each_folder}个文件");
        # 记录到了一定文件个数就换文件夹
        folder_count = 0;
        # 记录文件个数
        file_count = 1;
        # 所有二级文件夹
        for i in range(two_tier_folder_nums):
            folder_path = f"{path}/2tier_{folder_count}";
            # 一个二级文件夹写入数据
            for tier_num in range(2, tier_nums + 1):
                if tier_num > 2:
                    folder_path += f"/{tier_num}tier";
                for file_num in range(file_num_each_folder):
                    file_path = folder_path + r"/test" + str(file_count) + ".txt";
                    with open(file_path, mode="a", encoding="utf-8") as f:
                        f.write(f"{txt_content}\n现在时间是{time.time()}\n这是第{file_count}个文件啊！！！");
                    file_count += 1;
                else:
                    log.info(f"第{file_count // file_num_each_folder}个文件夹的文件创建完毕！")
            folder_count += 1;
        log.info("所有文件创建完毕！");
    else:
        log.warning("文件个数没有大于零，不创建文件！");


# 创建根路径
def create_root_path(content: dict):
    path = content.get("root_path");
    os.mkdir(path);


# 获取yaml文件的内容
def get_yml_data():
    yml_path = "create.yml";
    with open(yml_path, mode="r", encoding="utf-8") as f:
        # 读取yaml的文件内容（dict格式）
        content = yaml.load(f, yaml.FullLoader);
    int(content.get("file_nums"));
    int(content.get("two_tier_folder_nums"));
    int(content.get("tier_nums"));
    return content;


if __name__ == '__main__':
    try:
        content = get_yml_data();
        create_root_path(content);
        create_folder(content);
        create(content);
        os.system("pause");
    except Exception as e:
        # 异常：路径下文件夹已存在，路径下父级文件夹不存在，yaml格式错误，转换int类型错误
        log.error(e);
        os.system("pause");
