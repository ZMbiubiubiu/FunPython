#! /home/bingo/anaconda3/bin/python
# *- coding=utf-8 -*

__author__ = "ZzLee"
__date__ = "2019/04/27"
__mail__ = "zhangmeng.lee@foxmail.com"
__version__ = "1.0"


import os
import click

@click.command()
@click.argument('file')
@click.option(
    '--number',
    '-n',
    default=10,
    help="设置默认打印出的行数",
)
def head(number, file):
    """
        打印文件内容,默认前十行,可自己确定
        想要打印的行数大于文件实际的行数, 则输出实际的文件行数
    """
    # 获取文件的绝对路径
    path = os.path.abspath(file)
    with open(path) as f:
        for index, line in enumerate(f):
            if index == number:
                break
            print(index+1, line, sep='\t', end="")

if __name__ == "__main__":
    head()