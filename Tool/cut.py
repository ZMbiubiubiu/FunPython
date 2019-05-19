#! /home/bingo/anaconda3/bin/python
# *- coding=utf-8 -*

__author__ = "ZzLee"
__date__ = "2019/04/27"
__mail__ = "zhangmeng.lee@foxmail.com"
__version__ = "1.0"

import os
import click

PWD = os.getcwd()

@click.command()
@click.argument('file')
@click.option(
    '--delimiter',
    '-d',
    default=" ",
    help="指定分割字段",
)
@click.option(
    '--fields',
    '-f',
    default=None,
    help="只选择特定列,从1开始计数.2,4表示取第2/第4列,2:4表示取第二到第四列",
)
def cut(file,delimiter, fields):
    """
        实现cut命令 d f 选项
        d: 表示分割字段
        f: (1) 2:3 表示取第二列第三列
           (2) 2,4 表示取第二列和第四列
    """
    print(f'delimiter {delimiter}')
    file_path = os.path.join(PWD, file)
    with open(file_path, 'r') as f:
        for index, line in enumerate(f):
            bunk = line.split(delimiter)
            if fields == None:
                print(index+1,'  '.join(bunk))
            else:
                if ':' in fields: # 表示连续取某几列
                    tmp = fields.split(":")
                    if fields.endswith(":"):
                        bunk = bunk[int(tmp[0])-1:]
                    elif fields.startswith(":"):
                        bunk = bunk[0:int(tmp[1])]
                    else:
                        bunk = bunk[int(tmp[0])-1:int(tmp[1])]
                else:
                    tmp = fields.split(",")
                    bunk = [bunk[int(i)-1] for i in tmp]
                print(index+1,"  ".join(bunk))
if __name__ == "__main__":
    cut()