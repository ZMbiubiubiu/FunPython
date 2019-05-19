# stat_word_currences.py
# Created: 4 29 2019

"""
统计文件中各个单词出现的位置和次数
"""

__author__ = 'ZzLee'
__email__ = 'zhangmeng.lee@foxmail.com'
__version__ = '1.0'

import re
import sys
import click

# 匹配单词
WORD_RE = re.compile(r'\w+')


stat = {}
with open(sys.argv[1], encoding="utf-8") as f:
    for line_num, line in enumerate(f, 1): # 行数从1开始计
        for matched in WORD_RE.finditer(line):
            word = matched.group()
            column_num = matched.start() + 1
            location = (line_num, column_num) # 获得该单词的坐标, 第几行第几列
            stat.setdefault(word, []).append(location)


for word in sorted(stat, key=str.lower):
    print(word, stat[word])
    