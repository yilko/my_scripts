import os

import yaml

'''实现批量造csv数据'''
class LoginData:

    def __init__(self):
        yml_content = LoginData.get_yml_data();
        # print(yml_content);
        self.name = yml_content["name"];
        self.csv_path = yml_content["csv_path"];
        self.nums = int(yml_content["nums"]);

    # 获取yml的配置信息
    @staticmethod
    def get_yml_data():
        yml_path = "login_data.yml";
        with open(yml_path, mode="r", encoding="utf-8-sig") as f:
            # 读取yaml的文件内容（dict格式）
            return yaml.load(f, yaml.FullLoader);

    # 文件输入内容并打开文件
    def create_file(self):
        with open(self.csv_path, "w", encoding="utf-8-sig") as f:
            for num in range(self.nums):
                mail = f"{self.name}{num}@qq.com";
                f.write(f"{mail},{self.name}{num}\n");
        os.startfile(self.csv_path);


if __name__ == '__main__':
    LoginData().create_file();