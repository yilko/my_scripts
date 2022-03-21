import os, re, requests;
from bs4 import BeautifulSoup;

'''实现爬取煎蛋网的图片'''


class PaHs:
    # 获取每一页的页数url
    @staticmethod
    def page_nums(nums):
        url = "http://jandan.net/girl";
        url_ls = [];
        url_ls.append(url);
        print("正在获取图片地址...")
        for i in range(nums - 1):
            resp = requests.get(url);
            soup = BeautifulSoup(resp.text, "lxml");
            href_url = soup.find("a", title="Older Comments").get("href");
            url = "http:" + href_url;
            url_ls.append(url);
        else:
            print("获取图片地址成功...")
        return url_ls;

    # 定位图片的地址
    @staticmethod
    def loc_img(url_ls):
        img_ls = [];
        for url in url_ls:
            resp = requests.get(url);
            soup = BeautifulSoup(resp.text, "lxml");
            tag_ls = soup.find_all("img", attrs={"referrerpolicy": "no-referrer"});
            for i in tag_ls:
                # 获取的标签是bytes类型，需要转成str
                img = re.findall('src="(.+?)"/>', str(i))[0];
                img_url = f"http:{img}";
                img_ls.append(img_url);
        else:
            print("图片准备下载...");
        return img_ls;

    # 下载图片
    @staticmethod
    def download_img(img_ls):
        img_count = 0;
        for url in img_ls:
            if img_count % 10 == 0 and img_count != 0:
                print(f"已经下载了{img_count}张了！")
            file_name = url.split("/")[-1];
            with open(f"down_img/{file_name}", "wb") as f:
                resp = requests.get(url);
                # 这里要用content，因为content是二进制内容，text是文本
                f.write(resp.content);
            img_count += 1;
        else:
            print(f"所有图片下载完毕！总有{img_count}张");


if __name__ == '__main__':
    try:
        os.mkdir("./down_img");
        url_ls = PaHs.page_nums(30);
        img_ls = PaHs.loc_img(url_ls);
        PaHs.download_img(img_ls);
        os.system("pause");
    except Exception as e:
        print(e);
        os.system("pause");
