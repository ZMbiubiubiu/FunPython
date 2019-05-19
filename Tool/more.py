#! /home/bingo/anaconda3/bin/python
# *- coding=utf-8 -*

__author__ = "ZzLee"
__date__ = "2019/04/27"
__mail__ = "zhangmeng.lee@foxmail.com"
__version__ = "1.0"

"""
    模拟more命令
    自定义每次显示的函数， 默认每次显示十行文本
"""

import os
import click

class LineNumber(click.ParamType):
    name = 'line-number'
    def convert(self, value, params, ctx):
        flag = isinstance(value, int)
        if not flag:
            self.fail(
                f'{value} is not a int',
                params,
                ctx,
            )
        return value

@click.command()
@click.option(
    '--line-number',
    '-l',
    default=10,
    # type=LineNumber(),
)
@click.argument('file')
def show(file,line_number):
    with open(file) as f:
        data = f.read()
    lines = data.splitlines()
    while lines:
        chunk = lines[:line_number]
        lines = lines[line_number:]
        for line in chunk:
            print(line)
        if lines and input("要继续显示剩下的内容吗？['Y', 'y'] : ") in ["Y", "y"]:
            continue
    

if __name__ == "__main__":
    show()
    # 调用格式： python more.py -l 12 test.txt