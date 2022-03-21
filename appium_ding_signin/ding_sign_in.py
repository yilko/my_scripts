import configparser, os, time;
from appium import webdriver;
from selenium.webdriver.common.by import By;
from apscheduler.schedulers.blocking import BlockingScheduler;

'''实现钉钉自动打卡'''


class DingSignIn:
    config_dict = {};

    def __init__(self):
        config = configparser.ConfigParser();
        config_path = "ding_config.ini";
        config.read(config_path, encoding="utf-8");
        sections_ls = config.sections();
        for section in sections_ls:
            # keys = config.options(section);
            # 这个方法大小写不敏感
            items = config.items(section);
            for key, value in items:
                self.config_dict[key] = value;

    # appium基本配置
    @staticmethod
    def desire_caps() -> dict:
        reset_str = DingSignIn.config_dict.get("noreset");
        # reset_bool = None;
        if reset_str.lower() == "true":
            reset_bool = True;
        elif reset_str.lower() == "false":
            reset_bool = False;
        else:
            raise Exception("noReset的值不是true或者false！请检查配置文件！")
        return {"platformName": DingSignIn.config_dict.get("platformname"),
                "platformVersion": DingSignIn.config_dict.get("platformversion"),
                "deviceName": DingSignIn.config_dict.get("devicename"),
                "noReset": reset_bool}

    # 检查屏幕是否亮起
    @staticmethod
    def check_screen() -> bool:
        screen_cmd = DingSignIn.config_dict.get("screen_cmd");
        # 这个方法只是执行，获取不到内容的(os.popen方法最优)
        # os.system(cmd_bright_screen);
        content = os.popen(screen_cmd).read();
        flag = content.strip().split("=")[1];
        if flag == DingSignIn.config_dict.get("screen_true"):
            return True;
        elif flag == DingSignIn.config_dict.get("screen_false"):
            return False;
        else:
            raise Exception("检查屏幕亮起出错!");

    # 检查屏幕是否解锁
    @staticmethod
    def check_unlock() -> bool:
        unlock_cmd = DingSignIn.config_dict.get("unlock_cmd");
        content = os.popen(unlock_cmd).read();
        flag = content.strip().split("=")[1];
        if flag == DingSignIn.config_dict.get("unlock_false"):
            return False;
        elif flag == DingSignIn.config_dict.get("unlock_true"):
            return True;
        else:
            raise Exception("检查屏幕解锁出错!");

    # 滑动出现解锁页面
    @staticmethod
    def swipe_up(driver: webdriver, swipe_time=400, times=1):
        screen_size = driver.get_window_size();
        x = screen_size["width"];
        y = screen_size["height"];
        print(f"手机屏幕大小---{x}---{y}");
        x0 = 0.5 * x;
        y0 = 0.75 * y;
        y1 = 0.25 * y;
        for i in range(times):
            driver.swipe(x0, y0, x0, y1, swipe_time);
            print("滑动成功！");

    # 手机解锁
    @staticmethod
    def unlock(driver: webdriver) -> bool:
        # 键盘位置对应的坐标---pwd_path = [(200, 1380), (840, 1750), (520, 1750), (200, 1750)];
        pwd_str = DingSignIn.config_dict.get("pwd");
        for i in range(len(pwd_str)):
            pwd_path = f"//*[@text={pwd_str[i]}]";
            driver.find_element(By.XPATH, pwd_path).click();
        time.sleep(1);
        if DingSignIn.check_unlock():
            print("手机解锁成功！")
            return True;
        else:
            print("手机解锁失败！");
            return False;

    # 屏幕亮起和解锁四种情况
    def phone_case(self, driver: webdriver, screen_flag: bool, unlock_flag: bool) -> bool:
        if screen_flag is False and unlock_flag is False:
            print("进入未亮屏未解锁的场景");
            screen_open_cmd = DingSignIn.config_dict.get("screen_open_cmd");
            os.popen(screen_open_cmd).read();
            time.sleep(1)
            self.swipe_up(driver);
            time.sleep(1);
            unlock_flag = self.unlock(driver);
            return unlock_flag;
        elif screen_flag is True and unlock_flag is False:
            print("进入已亮屏未解锁的场景");
            self.swipe_up(driver);
            time.sleep(1);
            unlock_flag = self.unlock(driver);
            return screen_flag and unlock_flag;
        elif screen_flag is False and unlock_flag is True:
            raise Exception("不存在屏幕没亮但是已解锁的场景");
        elif screen_flag and unlock_flag:
            print("进入已亮屏已解锁的场景");
            return screen_flag and unlock_flag;

    # 打开钉钉实现打卡操作
    @staticmethod
    def ding_operation(driver: webdriver, case_flag: bool):
        if case_flag is True:
            driver.start_activity(DingSignIn.config_dict.get("package"),
                                  DingSignIn.config_dict.get("activity"));
            # 查看当前活动--adb shell dumpsys activity activities | findstr mResumedActivity
            # driver.wait_activity(DingSignIn.config_dict.get("curr_activity"), 60, interval=2);
            # print(driver.current_activity);
            # time.sleep(5)
            driver.implicitly_wait(20);
            # 点击工作台
            try:
                # 如果是无线连接可能会报以下错误
                # Original error: 'POST /element' cannot be proxied to UiAutomator2 server because the instrumentation process is not running (probably crashed)
                work_bench_loc = DingSignIn.config_dict.get("work_bench_loc");
                work_bench = driver.find_element_by_android_uiautomator(work_bench_loc);
                driver.implicitly_wait(20);
            except Exception as e:
                print(f"定位元素error!----{e}");
            else:
                work_bench.click();
            # 点击考勤打卡
            try:
                kaoqin_loc = DingSignIn.config_dict.get("kaoqin_loc");
                kaoqin = driver.find_element_by_android_uiautomator(kaoqin_loc);
                driver.implicitly_wait(20);
            except Exception as e:
                print(f"定位元素error!----{e}");
            else:
                kaoqin.click();
                print("打卡成功!!")
            # 点击打卡
            # clock_in_loc = DingSignIn.config_dict.get("clock_in_loc");
            # clock_in = driver.find_element_by_android_uiautomator(clock_in_loc);
            # driver.implicitly_wait(20);
            # clock_in.click();
        else:
            raise Exception(f"case_flag为{case_flag}")

    # 关闭钉钉
    def close(self, driver: webdriver):
        # 关闭不能使用driver.close_app()，因为driver是对于手机桌面的
        driver.terminate_app(driver.current_package);
        driver.quit();
        if self.check_screen():
            screen_open_cmd = self.config_dict.get("screen_open_cmd");
            os.popen(screen_open_cmd).read();
            print("退出钉钉成功，已息屏");

    # 主程序入口
    def main(self):
        desired_caps = das.desire_caps();
        print(desired_caps);
        driver = webdriver.Remote(das.config_dict.get("url"), desired_caps);
        # 测试未亮屏未解锁的场景
        # time.sleep(10);
        screen_flag = self.check_screen();
        unlock_flag = self.check_unlock();
        case_flag = self.phone_case(driver, screen_flag, unlock_flag);
        self.ding_operation(driver, case_flag);
        self.close(driver);

    # 定时任务
    def timing(self):
        block_sched = BlockingScheduler(timezone="Asia/Shanghai");
        block_sched.add_job(self.main, "cron", day_of_week="1-6", hour="11", minute="40,39");
        block_sched.start();


if __name__ == '__main__':
    das = DingSignIn();
    das.timing();
    # das.main();
