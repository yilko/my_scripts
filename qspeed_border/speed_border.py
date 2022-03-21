'''
1.收到别人弹窗邀请自动关闭--测试通过
2.大厅时断网重试2次，连不上网息屏(人为介入搞定网络，该操作只是息屏省电)--测试通过
3.返回房间中网络波动导致在边境页面，自动重新进房开始--测试通过
4.游戏途中断开连接返回大厅，自动重新进房开始--测试通过
5.匹配超时自动再点匹配--测试通过
6.支持无人跑图时提高音量作为提醒--测试通过
7.支持10分钟没结束自动退出，自动重新进房开始--测试通过
8.次数为零和时间已到手机自动息屏--测试通过
'''

from airtest.core.api import *;

'''实现飞车挂边境'''

# 三条/默认取当前连接中的第一台手机
# auto_setup(__file__, devices=["Android:///"]);
auto_setup(__file__, devices=["Android://127.0.0.1:5037/设备名"]);
# auto_setup(__file__, devices=["Android://127.0.0.1:5037/192.168.199.233:5555"]);
pic_border_path = r"D:\airtest_img\speed\进边境";
exception_loc = r"D:\airtest_img\speed\异常退出定位";


# 关闭别人的弹窗邀请
def close_invite():
    if exists(Template(pic_border_path + r"\邀请.png")):
        click(Template(pic_border_path + r"\关闭邀请.png"));


# 确定出现异常后在哪个位置
def find_loc():
    # 判断是否被邀请页面挡住其他页面
    close_invite();
    # 在边境房间
    if exists(Template(exception_loc + r"\在边境房间.png")):
        start_loc = wait(Template(pic_border_path + r"\开始匹配.png"), timeout=10, interval=1);
        close_invite();
        click(start_loc);
    # 在边境页面
    elif exists(Template(exception_loc + r"\在边境页面.png")):
        border_to_room();
    # 在大厅
    elif exists(Template(exception_loc + r"\在大厅.png")):
        home_to_border_room();
    # 在排位页面
    elif exists(Template(exception_loc + r"\在排位页面.png")):
        rank_to_room();
    # 在断网重连提示页面
    elif exists(Template(exception_loc + r"\断开重试.png")):
        count = 0;
        while exists(Template(exception_loc + r"\断开重试.png")):
            # 如果2次重试都不行，说明断网了，手机息屏省电，等待发现解决该问题
            if count == 2:
                keyevent("26");
                raise Exception("断网了！关机息屏");
            click(Template(exception_loc + r"\断开连接点确定.png"));
            sleep(40);
            count += 1;
    else:
        keyevent("26");
        raise Exception("没有匹配到对应的页面！关机息屏");


# 从大厅进去到边境界面
def home_to_border_room():
    match_loc = wait(Template(pic_border_path + r"\赛事比赛.png"), timeout=30, interval=1);
    close_invite();
    click(match_loc);
    rank_to_room();


# 从排位页面进入边境房间
def rank_to_room():
    border_loc = wait(Template(pic_border_path + r"\边境战争.png"), timeout=30, interval=1);
    close_invite();
    click(border_loc);
    sleep(1);
    border_to_room();


# 从边境页面进入房间
def border_to_room():
    single_run_loc = wait(Template(pic_border_path + r"\个人竞速.png"), timeout=30, interval=1);
    close_invite();
    click(single_run_loc);
    coupon_60_loc = wait(Template(pic_border_path + r"\60点券.png"), timeout=30, interval=1);
    close_invite();
    click(coupon_60_loc);
    game_end();


# 未到开放时间或次数为零自动息屏
# 在边境页面和房间两个情况都有，都要考虑
def game_end():
    eleven = exists(Template(pic_border_path + r"\11点.png"));
    full = exists(Template(pic_border_path + r"\房间弹窗提示次数已满.png", threshold=0.9));
    zero = exists(Template(pic_border_path + r"\边境页面次数为0.png"));
    if full:
        print(full);
        keyevent("26");
        raise Exception("房间弹窗，次数没了，息屏！");
    elif zero:
        print(zero);
        keyevent("26");
        raise Exception("边境页面，次数没了，息屏！");
    elif eleven:
        print(eleven)
        keyevent("26");
        raise Exception("到点了，息屏！");
    # else:
    #     raise Exception("game end方法有误！");


# 循环进行边境开始结束(大概3分钟一局)
def border_start_end():
    voice_max = None;
    while True:
        try:
            start_loc = wait(Template(pic_border_path + r"\开始匹配.png"), timeout=10, interval=1);
            close_invite();
            click(start_loc);
        except TargetNotFoundError:
            # 解决网络不稳定回到边境页面(或其他原因回到大厅)的问题
            find_loc();
            continue;
        try:
            wait(Template(pic_border_path + r"\放弃禁用.png"), timeout=50, interval=1);
        except TargetNotFoundError:
            # 没有出现禁图界面可能是到点或者没次数了
            game_end();
            # 没有识别到可能是匹配超时，直接再点一次匹配(解决匹配超时回到房间的问题)
            continue;
        for i in range(4):
            sleep(35);
            # 解决断网后回到大厅的问题
            if exists(Template(exception_loc + r"\断开连接_返回大厅.png")) or exists(
                    Template(exception_loc + r"\加载超时_游戏已开始.png")):
                click(Template(exception_loc + r"\断开连接点确定.png"));
                sleep(2);
                # 确定后回到首页，直接下个循环，找不到图片重新调用find_loc()
                continue;
            # 80秒如果还是第一说明没人跑，此时音量调到最大提醒(80秒就相当于开局20秒，其中的60秒在游戏加载)
            if i == 1 and exists(Template(pic_border_path + r"\第一.png")):
                voice_max = True;
                for j in range(16):
                    keyevent("24");
        # 结束页面返回房间
        for i in range(15):
            try:
                wait(Template(pic_border_path + r"\结束头像.png"), timeout=60, interval=2);
            except TargetNotFoundError:
                if i == 0:
                    voice_max = True;
                    # 140+60秒都没结束可能是没人跑，此时音量调到最大提醒
                    for j in range(16):
                        keyevent("24");
            else:
                # 如果有调过音量，那么在结算页面把音量调小
                if voice_max:
                    voice_max = False;
                    for j in range(15):
                        keyevent("25");
                try:
                    go_on = wait(Template(pic_border_path + r"\点击继续.png", threshold=0.3), timeout=10, interval=0.5);
                except TargetNotFoundError:
                    click(Template(pic_border_path + r"\结算第一.png", threshold=0.3))
                else:
                    click(go_on);
                back_loc = wait(Template(pic_border_path + r"\返回.png"), timeout=10, interval=0.5);
                click(back_loc);
                sleep(8);
                break;
        # 等十分钟如果还没结束，那么手动退出再开一局
        else:
            # 如果有调过音量，那么在重新开局时音量调小
            if voice_max:
                voice_max = False;
                for j in range(15):
                    keyevent("25");
            double_click(Template(pic_border_path + r"\设置.png", threshold=0.3));
            one_exit = wait(Template(pic_border_path + r"\退出本局.png"), timeout=10, interval=1);
            click(one_exit);
            two_exit = wait(Template(pic_border_path + r"\二次确认退出.png"), timeout=10, interval=1);
            click(two_exit);
            sleep(2);
            # 确定后回到首页，直接下个循环，找不到图片重新调用find_loc()
            continue;


if __name__ == '__main__':
    border_start_end();
