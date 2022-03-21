import random
import time
import pygame
'''实现有雪花的动态圣诞树'''


class Snows:
    def __init__(self):
        pygame.init();
        bg_img = "tree.png";
        self.bg_size = (622, 706);
        self.screen = pygame.display.set_mode(self.bg_size);
        pygame.display.set_caption("圣诞快乐！")
        self.bg = pygame.image.load(bg_img);

    def create_snows(self):
        snow_ls = [];
        for i in range(150):
            x_loc = random.randrange(0,self.bg_size[0]);
            y_loc = random.randrange(0,self.bg_size[1]);
            x_offset = random.randint(-1, 1);
            snow_size = random.randint(4, 6);
            snow_ls.append([x_loc, y_loc, x_offset, snow_size]);
        # 创建时钟对象
        clock = pygame.time.Clock();
        done = False;
        while not done:
            # 消息事件循环，判断退出
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True;
            self.screen.blit(self.bg, (0,0))
            # 雪花列表循环
            for i in range(len(snow_ls)):
                # 绘制雪花，颜色、位置、大小
                pygame.draw.circle(self.screen, (255, 255, 255), snow_ls[i][:2], snow_ls[i][3] - 3)
                # 移动雪花位置（下一次循环起效）
                snow_ls[i][0] += snow_ls[i][2]
                snow_ls[i][1] += snow_ls[i][3]
                # 如果雪花落出屏幕，重设位置
                if snow_ls[i][1] > self.bg_size[1]:
                    snow_ls[i][1] = random.randrange(-50, -10)
                    snow_ls[i][0] = random.randrange(0, self.bg_size[0])
            # 刷新屏幕
            pygame.display.flip()
            clock.tick(30)
        # 退出
        pygame.quit()


    def play_music(self):
        # 添加音乐
        pygame.mixer.music.load('two_you_part.mp3')  # 加载音乐文件
        pygame.mixer.music.play()  # 播放音乐流
        pygame.mixer.music.fadeout(600000)  # 设置音乐结束时


if __name__ == '__main__':
    snows = Snows();
    snows.play_music();
    snows.create_snows();
