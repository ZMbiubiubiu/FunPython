__author__ = "ZzLee"
__date__ = "2019/05/27"
__mail__ = "zhangmeng.lee@foxmail.com"
"""
    生命游戏的四个规则：
    (1)如果一个细胞为ON, 邻居中少于两个为ON, 它变成OFF
    (2)如果一个细胞为ON, 邻居中有两个或者三个为ON, 它还为ON
    (3)如果一个细胞为ON, 邻居中超过3个为ON, 它变成OFF
    (4)如果一个细胞为OFF, 邻居中恰好有3个为ON, 它变成ON
"""


import click 
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.animation as animation 

ON = 255
OFF = 0


def randomGrid(N):
    """初始状态为随机的图形""" 
    return np.random.choice([255, 0], N*N, [0.5, 0.5]).reshape(N, N)

def gliderGrid(N, i=1, j=1):
    """初始状态为滑翔机图案""" 
    grid = np.zeros(N*N).reshape(N, N)
    glider = np.array([
        [0, 0, 255],
        [255, 0, 255],
        [0, 255, 255],
    ])
    grid[i:i+3, j:j+3] = glider 
    return grid 

def gosperGrid(N, i=1, j=1):
    """初始状态为高斯帕滑翔机图案""" 
    grid = np.zeros(N*N).reshape(N, N)
    gosper = np.array([
        [0, 0, 255],
        [0, 0, 255],
        [0, 0, 255],
    ])
    grid[i:i+3, j:j+3] = gosper 
    return grid 
METHOD_DICT = { # 棋盘初始化方法的映射关系
    'random' : randomGrid,
    'glider' : gliderGrid,
    'gosper' : gosperGrid,
}

def update(frame_num, img, grid, N):
    """更新生命游戏图案"""
    new_grid = grid.copy()
    for i in range(N):
        for j in range(N):
            # 根据游戏规则来进行更新当前区域ON/OFF(判断相邻的8个节点)
            # 分层计算
            total = int(
                grid[(i-1)%N][(j-1)%N]+grid[(i-1)%N][j]+grid[(i-1)%N][(j+1)%N] + 
                grid[i][(j-1)%N]+grid[i][(j+1)%N] + 
                grid[(i+1)%N][(j-1)%N]+grid[(i+1)%N][j]+grid[(i+1)%N][(j+1)%N]
            ) / 255

            if grid[i][j] == ON:
                if total < 2 or total > 3:
                    new_grid[i][j] = OFF
            else:
                # 当前无生命
                if total == 3:
                    new_grid[i][j] = ON
    # 更新一次
    img.set_data(new_grid)
    grid[:] = new_grid[:]
    return img 

@click.command()
@click.argument( # 必选参数
    'method',
    default='random',
    type = click.Choice(['random', 'glider', 'gosper']), # 接受的参数值
    # help="设置初始图案",
)
@click.option( # 可选参数
    '--grid-size',
    # '-s',
    # nargs=1, # 接受的参数个数
    default=100, # 默认值
    help="设置生命游戏的棋盘大小",     # 提示帮助
)
@click.option(
    '--interval',
    # '-i',
    # nargs=1,
    default=50,
    help="设置生成的动画的时间间隔",
)
def main(method, grid_size, interval):
    """游戏的主逻辑"""
    # 生成棋盘
    grid_method = METHOD_DICT[method]
    grid = grid_method(grid_size)

    # 设置动画
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation="nearest")
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, grid_size,),
                                    frames=10,
                                    interval=interval,
                                    save_count=50
    )
    plt.show()


if __name__ == "__main__":
    main()
