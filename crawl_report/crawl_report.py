# -*- coding:utf-8 -*-
import os, yaml, random, requests;
from config_log import ConfigLog;
'''实现爬取巨潮网页的指定大小pdf'''

log = ConfigLog().config_log();
# 随机代理
user_agent = [
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0"
];


class CrawlReport:
    def __init__(self):
        yml_path = "report.yml";
        with open(yml_path, mode="r", encoding="utf-8") as f:
            # 读取yaml的文件内容（dict格式）
            content = yaml.load(f, yaml.FullLoader);
        self.time_range = content.get("time_range");
        self.column = content.get("column");
        self.category = content.get("category");
        self.min_size = int(content.get("min_size"));
        self.max_size = int(content.get("max_size"));

    # 根据不同的板块选择不同的类别
    def __deal_category(self) -> list:
        # 所有类别
        if self.category is None:
            # 深沪京类别
            if self.column == "szse":
                return [
                    "category_ndbg_szsh", "category_bndbg_szsh", "category_yjygjxz_szsh", "category_dshgg_szsh",
                    "category_jshgg_szsh", "category_gddh_szsh", "category_rcjy_szsh", "category_gszl_szsh"
                ];
            # 三板类别
            elif self.column == "third":
                return ["category_lsgg"];
            # 基金类别
            elif self.column == "fund":
                return ["category_jdbg_jjgg", "category_qt_jjgg"];
            # 债券类别
            elif self.column == "bond":
                return ["category_zqqt_zqgg"];
        # 深沪京多选的类别
        elif ";" in self.category:
            return self.category.split(";");
        # 深沪京单选类别
        else:
            return [self.category];

    # 获取公司的信息(名字，pdf等)
    def get_company_info(self) -> list:
        category_ls = self.__deal_category();
        data_ls = [];
        url = "http://www.cninfo.com.cn/new/hisAnnouncement/query";
        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                   "User-Agent": random.choice(user_agent)};
        log.info(f"正在筛选大小范围在{self.min_size}m-{self.max_size}m之间的pdf文件");
        for category in category_ls:
            data = {
                "pageNum": 1,  # 页数
                "pageSize": "30",  # 每页显示30条
                "column": self.column,  # 板块
                "tabName": "fulltext",  # 公告
                "category": category,  # 报告类别
                "seDate": self.time_range  # 查询时间
            };
            resp = requests.post(url, data, headers=headers);
            log.debug(f"总共条数-totalAnnouncement-{resp.json()['totalAnnouncement']}");
            # 计算页数,如果大于100页只取前100页的值，如果整除页数-1，因为接口只返回前100条数据
            total_nums = int(resp.json().get("totalAnnouncement"));
            page_nums = (total_nums // 30) + 1;
            if page_nums > 100:
                page_nums = 100;
            elif total_nums % 30 == 0:
                page_nums -= 1;
            log.info(f"当前在循环{self.column}板块的{category}类别，总页数是{page_nums}");
            for i in range(1, page_nums + 1):
                data["pageNum"] = i;
                headers["User-Agent"] = random.choice(user_agent);
                resp = requests.post(url, data, headers=headers);
                company_data_ls = resp.json().get("announcements");
                conform_company_data = self.__check_size(company_data_ls, i);
                # 获取多个不同的类别可能会有重复的pdf，做去重处理
                for i in conform_company_data:
                    data_ls.append(i) if i not in data_ls else log.debug(f"存在重复pdf文件===={i},只保留一份,已去重");
            log.info(f"{category}类别筛选完毕！");
        log.info(f"总共有{len(data_ls)}个pdf文件符合条件！");
        log.debug(data_ls);
        return data_ls;

    # 判断文件的大小范围进行过滤
    def __check_size(self, company_data: list, page_nums: int) -> list:
        down_urls = [];
        for company in company_data:
            if isinstance(self.min_size, (int, float)) and isinstance(self.max_size, (int, float)):
                if self.min_size * 1024 <= company.get("adjunctSize") <= self.max_size * 1024:
                    pdf_name = f"{company.get('secName')}-{company.get('announcementTitle')}";
                    url = f"http://static.cninfo.com.cn/{company.get('adjunctUrl')}";
                    down_urls.append({pdf_name: url});
        else:
            log.debug(f"第{page_nums}页共有{len(down_urls)}个文件符合");
        return down_urls;

    # 保存pdf到指定路径
    @staticmethod
    def save_pdf(folder_name, data_ls: list):
        if not os.path.exists(folder_name):
            os.mkdir(folder_name);
        count = 0;
        log.info(f"正在准备下载pdf文件...")
        for data_dict in data_ls:
            for key, value in data_dict.items():
                new_key = key[1:] if key.startswith("*") else key;
                with open(f"{folder_name}/{count + 1}.{new_key}.pdf", "wb") as f:
                    resp = requests.get(value);
                    # content是二进制内容,text是文本,pdf本身是二进制文件
                    f.write(resp.content);
            else:
                count += 1;
                if count % 10 == 0:
                    log.info(f"已经下载了{count}个pdf文件了！");
        else:
            log.info(f"所有pdf文件下载完毕！总共有{count}个文件，已下载到当前{folder_name}文件夹下！");


if __name__ == '__main__':
    try:
        cr = CrawlReport();
        pdf_ls = cr.get_company_info();
        cr.save_pdf("pdf_files", pdf_ls);
        os.system("pause");
    except Exception as e:
        log.info(e);
        os.system("pause");
