import random;
import turtle;
import os;
'''画出圣诞树'''


class Tree:
    def __init__(self):
        turtle.screensize(800, 600, "#363636");
        # pygame.init();
        # screen = pygame.display.set_mode((800,600));

    # 获取画笔
    @staticmethod
    def get_pen(shape: str, color: str, speed: int) -> turtle:
        pen = turtle.Turtle();
        pen.shape(shape);
        pen.color(color);
        pen.speed(speed);
        pen.penup();
        return pen;

    # 去指定位置打印图形
    @staticmethod
    def go_and_stamp(pen: turtle, x: float, y: float) -> None:
        pen.goto(x, y);
        pen.stamp();

    # 画出星星
    @staticmethod
    def paint_star() -> None:
        star_pen = Tree.get_pen("classic", "#FFEC8B", 10);
        star_pen.goto(-20, 270);
        star_pen.pendown();
        star_pen.fillcolor("#FFEC8B");
        star_pen.begin_fill();
        for i in range(5):
            star_pen.forward(40);
            star_pen.right(144);
        star_pen.end_fill();
        star_pen.hideturtle();

    # 画出树叶
    @staticmethod
    def paint_leaf(rows: int) -> int:
        triangle_pen = Tree.get_pen("triangle", "#A2CD5A", 10);
        triangle_pen.left(90);
        k = 0;
        for i in range(1, int(rows) + 1):
            y = 10 * i
            for j in range(i - k):
                x = 10 * j
                Tree.go_and_stamp(triangle_pen, -x, 250 - y);
                Tree.go_and_stamp(triangle_pen, x, 250 - y);
            # 每四行要重新计算三角形每行的个数
            if i % 4 == 0:
                k += 2;
        return 250 - 10 * rows;

    # 画出树枝
    @staticmethod
    def paint_branch(leaf_y: int) -> int:
        branch_y = None;
        branch_pen = Tree.get_pen("square", "#8B4513", 10);
        for i in range(1, 5):
            y = 15 * i;
            for j in range(2):
                x = 10 * j;
                Tree.go_and_stamp(branch_pen, x, leaf_y - y);
                Tree.go_and_stamp(branch_pen, -x, leaf_y - y);
                branch_y = leaf_y - y;
        return branch_y;

    # 画出雪花
    @staticmethod
    def paint_snow() -> None:
        snow_ls = [];
        snow_pen = Tree.get_pen("classic", "#FFFAFA", 10);
        snow_pen.pensize(2);
        snow_pen.hideturtle();
        for i in range(100):
            x_loc = random.randrange(-380, 380);
            y_loc = random.randrange(-280, 280);
            x_offset = random.randint(-1, 1);
            snow_size = random.randint(3, 6);
            snow_ls.append([x_loc, y_loc, x_offset, snow_size]);
            for j in range(6):
                snow_pen.penup();
                snow_pen.goto(x_loc, y_loc);
                snow_pen.pendown();
                snow_pen.forward(snow_size);
                snow_pen.backward(snow_size);
                snow_pen.right(60);

    # 播放音乐
    @staticmethod
    def play_music() -> None:
        os.system(r"F:\zk_project\util\two_you.mp3");

    # 输出文字
    @staticmethod
    def write(branch_y: int) -> None:
        word_pen = Tree.get_pen("classic","#FFC125",10);
        word_pen.goto(-70,branch_y-80);
        font = ("微软雅黑",18,"italic");
        word_pen.write("张绮梦小包被 ",font=font);
        word_pen.goto(-95, branch_y - 110);
        word_pen.write("Merry Christmas! ", font=font);
        word_pen.hideturtle();


    # 输出成品
    def paint_product(self):
        # Tree.play_music();
        Tree.paint_star();
        leaf_y = Tree.paint_leaf(32);
        branch_y = Tree.paint_branch(leaf_y);
        # Tree.paint_snow();
        # turtle.done();
        Tree.write(branch_y);
        turtle.exitonclick();


if __name__ == '__main__':
    Tree().paint_product();
