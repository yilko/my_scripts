import re
import requests
from bs4 import BeautifulSoup;

'''
爬取该网站的小说
http://www.yetianlian.com/
'''
def get_url():
    url_dict = {};
    resp = requests.get("http://www.yetianlian.com/yt376/");
    soup = BeautifulSoup(resp.text, "lxml");
    # 定位具体的标签，然后查找该标签下行所有兄弟节点
    dt_tag = soup.find("dt", text=re.compile("(.+?)正文卷"));
    dd_ls = dt_tag.find_next_siblings("dd");
    # print(len(dd_ls),dd_ls);
    # 标签列表遍历，拼接成{章节名：文章链接}这种形式
    for dd_tag in dd_ls:
        a_tag = dd_tag.find("a");
        url_dict[a_tag.string] = a_tag["href"];
    return url_dict;


def get_content(url_dict: dict):
    for k,v in url_dict.items():
        print(k,v);
        resp = requests.get(f"http://www.yetianlian.com/{v}");
        soup = BeautifulSoup(resp.text, "lxml");
        div_tag = soup.find("div", id="content", class_="showtxt");
        content_ls = [k];
        count = 0;
        # div_tag.strings是一个生成器，获取的内容有很多空格空行，需要进行排版
        for i in div_tag.strings:
            if "请记住本书首发域名" in str(i.strip()):
                break;
            if count % 2 == 0:
                # print(i.strip())
                content_ls.append(i.strip());
            count += 1;
        # print(content_ls)
        with open("file_template/test.txt","a",encoding="utf-8") as f:
            for line in content_ls:
                f.write(f"{line}\n");
            else:
                f.write("\n");


if __name__ == '__main__':
    url_dict = get_url();
    # print(len(url_dict), url_dict);
    get_content(url_dict);
