from datetime import datetime;
from aip import AipOcr;
from appium import webdriver;
from selenium.webdriver.common.by import By;
import pytesseract, re;
from PIL import Image;

'''实现两种图像识别的方式'''


def desire_caps() -> dict:
    return {
        "platformName": "Android",
        "platformVersion": "10",
        # 你的设备码,包名与活动名
        "deviceName": "xxxxx",
        "appPackage": "xxx",
        "appActivity": "xxxx",
        "noReset": True
    }


# 截图验证码图片，重命名并保存到相对路径下
def screen_save() -> str:
    time_now = datetime.now().strftime("%Y%m%d-%H%M");
    img_path = time_now + ".png";
    print("图片路径为" + img_path);
    return img_path;


# 调用百度的ocr图片识别
def baidu_ocr(img_path: str):
    # 你的百度id和key值
    APP_ID = "xxx";
    API_KEY = "xxx";
    SECRET_KEY = "xxx";
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY);
    with open(img_path, "rb") as f:
        result = client.basicGeneral(f.read())
    print("验证码为:" + result)
    return result["words_result"][0]["words"];


# 使用tesseract的ocr图片识别
def tesseract_ocr(img_path: str):
    img = Image.open(img_path);
    data = pytesseract.image_to_string(img);
    str_ls = re.findall(r"\d+", data);
    check_code = "";
    for i in range(len(str_ls)):
        check_code += str(str_ls[i]);
    print("验证码为:" + check_code);
    return check_code;


# 模拟一个登陆操作，识别图片验证码并输入
def cloud_operation(driver: webdriver):
    driver.find_element(By.ID, "id_frame").send_keys("text");
    driver.find_element(By.ID, "id_frame").send_keys("text");
    img_path = screen_save();
    driver.find_element(By.ID, "id_frame").screenshot(img_path);
    # driver.find_element(By.ID, "id_frame").send_keys(baidu_ocr(img_path));
    driver.find_element(By.ID, "id_frame").send_keys(tesseract_ocr(img_path));
    driver.find_element(By.ID, "id_frame").click();


if __name__ == '__main__':
    desired_caps = desire_caps();
    driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps);
    cloud_operation(driver);
