from airtest.core.api import *;

'''实现飞车登录'''

# 三条/默认取当前连接中的第一台手机
# auto_setup(__file__, devices=["Android:///"]);
auto_setup(__file__, devices=["Android://127.0.0.1:5037/设备名"]);
# auto_setup(__file__, devices=["Android://127.0.0.1:5037/192.168.199.233:5555"]);
pic_login_path = r"D:\airtest_img\speed\登录";
pic_close_path = r"D:\airtest_img\speed\关闭大厅弹窗";
exception_loc = r"D:\airtest_img\speed\异常退出定位";
pic_border_path = r"D:\airtest_img\speed\进边境";
keyevent("26");
start_app("com.tencent.tmgp.speedmobile");
sleep(25);


# 选择qq登录
def qq_login():
    click(Template(pic_login_path + r"\qq登录.png"));
    account_switch = wait(Template(pic_login_path + r"\选择其他账号登录.png"), timeout=10, interval=0.5);
    click(account_switch);
    sleep(2);
    choose_account = wait(Template(pic_login_path + r"\选择大号登录.png"), timeout=60, interval=1);
    click(choose_account);
    auth_login = wait(Template(pic_login_path + r"\授权登录.png"), timeout=10, interval=0.5);
    click(auth_login);
    sleep(1);
    auth_twice = wait(Template(pic_login_path + r"\允许授权.png"), timeout=10, interval=0.5);
    click(auth_twice);
    enter_game = wait(Template(pic_login_path + r"\进入游戏.png"), timeout=10, interval=0.5);
    click(enter_game);
    sleep(20);


# 同意协议并qq登录
def agree_and_login():
    agree = wait(Template(pic_login_path + r"\勾选同意.png"), timeout=30, interval=1);
    click(agree);
    sleep(1);
    qq_login()


# 默认选中大号登录
if exists(Template(pic_login_path + r"\18区.png")):
    enter_game = wait(Template(pic_login_path + r"\进入游戏.png"), timeout=10, interval=0.5);
    click(enter_game);
    sleep(20);
# 没有默认账号登录
elif exists(Template(pic_login_path + r"\qq登录.png")):
    if exists(Template(pic_login_path + r"\已勾同意.png")):
        qq_login();
    else:
        agree_and_login();
# 默认其他账号登录
else:
    sign_out = wait(Template(pic_login_path + r"\注销.png"), timeout=30, interval=1);
    click(sign_out);
    agree_and_login();

x1 = Template(pic_close_path + r"\x1.png", threshold=0.1, target_pos=3);
x2 = Template(pic_close_path + r"\x2.png", threshold=0.1, target_pos=3);
x3 = Template(pic_close_path + r"\x3.png", threshold=0.1, target_pos=3);
home = Template(exception_loc + r"\在大厅.png");
sleep(3);
while exists(home) is False:
    if exists(x1):
        click(x1);
        sleep(1);
    elif exists(x2):
        click(x2);
        sleep(1);
    elif exists(x3):
        click(x3);
        sleep(1);
match_loc = wait(Template(pic_border_path + r"\赛事比赛.png"), timeout=30, interval=1);
click(match_loc);
