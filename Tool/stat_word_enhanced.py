# stat_word_currences.py
# Created: 4 29 2019

"""
统计文件中各个单词出现的位置和次数,写成一个CLI的形式
子命令包括:
    location: 列举出各个单词出现的次数和位置
    normal:   仅仅列出各个单词出现的次数
"""

__author__ = 'ZzLee'
__email__ = 'zhangmeng.lee@foxmail.com'
__version__ = '1.0'

import re
import os
import click

# 验证输入的'文件'参数
# ps: 实际上没必要这么麻烦, 之所这么验证, 是为了练习 Click 库的使用
class FileValid(click.ParamType):
    name = 'file',
    def convert(self, value, params, ctx): # file, arguments and options, context of the command
        flag = os.path.isfile(value)
        if not flag:
            self.fail(
                f'{value} is not exist!',
                params,
                ctx,
            )
        return value

@click.group()
@click.argument(
    'file',
    type=FileValid(),
)
@click.pass_context
def main(ctx, file):
    """
    输入一个文件名, 统计其中单词出现的次数和位置
    stat_word_enhanced.py [OPTIONS] [FILE] COMMAND [ARGS]
    需要添加子命令
    location
    normal
    """
    WORD_RE = re.compile(r'\w+')
    stats = {}
    with open(file, encoding="utf-8") as f:
        for line_num, line in enumerate(f):
            for matched in WORD_RE.finditer(line):
                word = matched.group()
                column_num = matched.start() + 1
                location = (line_num, column_num)
                stats.setdefault(word, []).append(location)
    ctx.obj = {
        "stats" : stats,
    }

@main.command()
@click.pass_context
def location(ctx):
    stats = ctx.obj['stats']
    for word, location in stats.items():
        print('{:15}: {}\t {}'.format(word, len(location), location))

@main.command()
@click.pass_context
def normal(ctx):
        stats = ctx.obj['stats']
        for word, location in stats.items():
            print('{:15} : {}'.format(word, len(location)))

if __name__ == "__main__":
    main()