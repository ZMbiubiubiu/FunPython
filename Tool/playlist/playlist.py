#! /home/bingo/anaconda3/bin/python
# *- coding=utf-8 -*

__author__ = "ZzLee"
__date__ = "2019/04/27"
__mail__ = "zhangmeng.lee@foxmail.com"
__version__ = "1.0"

"""
    <python>极客项目编程
    代码重构,层次更加清晰,修改bug,并且使用新的命令行库click
"""

import re
import sys
import click
import plistlib
from matplotlib import pyplot
import numpy as np


def dealTracksToDict(file):
    """
        处理文件中的音轨信息,整理成一个字典
    """
    # 读取文件,保存成一个字典
    plist = plistlib.readPlist(file)
    # 获取文件中音轨信息, tracks是一个字典
    tracks = plist['Tracks']
    # 用字典来记录音轨信息
    tracks_dict = {}
    for id, track in tracks.items():
        # print(id, track)
        try:
            # 判断一个音轨是否重复,第一看名字,第二如果名字相同,看音轨长度
            name = track['Name']
            duration = track['Total Time']
            if name in tracks_dict and duration // 1000 == tracks_dict[name][0] // 1000:
                count = tracks_dict[name][1]
                tracks_dict[name] = (duration, count+1)
            else:
                tracks_dict[name] = (duration, 1)
        except:
            pass
    return tracks_dict


@click.group()
def main():
    pass

@main.command()
@click.argument('file')
def duplicates(file):
    """
        在一个播放列表中查找重复的音轨, 将信息(音轨的名字,重复的次数)保存到文件中
    """
    print(f'Finding duplicate tracks in {file}')
    # 用字典来记录音轨信息
    tracks_dict = dealTracksToDict(file)
    # print(tracks_dict)
    # 提取重复音轨, 保存到文件中
    duplicates_track = [(value[1], key) for key, value in tracks_dict.items() if tracks_dict[key][1] > 1]
    if len(duplicates_track) > 0:
        print(f'Found {len(duplicates_track)}. Track names saved to dups.txt')
    else:
        print("No duplicates tracks found!")
    
    with open('dups.txt','w',encoding='utf-8') as f:
        for dup in duplicates_track:
            f.write(f"[{dup[0]}] {dup[1]}\n")

@main.command()
@click.argument('files', nargs=-1)
def common(files):
    """
        在多个播放列表中找到相同的音轨
    """
    # 列表中每个元素是一个集合, 每个集合保存一个文件中的音轨信息
    total_tracks = []
    for file in files:
        # 记录信息
        single_tracks = dealTracksToDict(file)
        set_track = set()
        for key, val in single_tracks.items():
            set_track.add((key, val[0]))
        total_tracks.append(set_track)
    # 得到多个文件中音轨的交集
    common_tracks = set.intersection(*total_tracks)
    # 写入文件中
    if len(common_tracks) > 0:
        print(f'{len(common_tracks)} common tracks found.')
        with open('common.txt', 'w', encoding='utf-8') as f:
            for track in common_tracks:
                f.write(f'{track[0]}:{track[1]}')
                print(f'{track[0]}:{track[1]}')
    else:
        print("No common tracks.")

@main.command()
@click.argument('file')
def plot(file):
    """
        获取音轨的时长和排名,画两个图:散点图/柱状图
    """
    plist = plistlib.readPlist(file)
    tracks = plist["Tracks"]
    ratings = []
    durations = []
    for id, track in tracks.items():
        try:
            rating = track["Album Rating"]
            duration = track["Total Time"]
        except:
            pass
        else:
            ratings.append(rating)
            durations.append(duration)

    if len(ratings) == 0:
        print(f"No valid Album Rating/Total Time data in {file}")
        return -1
    x = np.array(durations, np.int32)
    # 转换成分钟
    x = x / 60000
    y = np.array(ratings, np.int32)
    pyplot.subplot(2, 1, 1)
    # 散点图
    pyplot.plot(x, y, 'o')
    pyplot.axis([0, 1.05*np.max(x), -1, 110])
    pyplot.xlabel('Track Duration')
    pyplot.ylabel('Track Rating')

    # 柱状图
    pyplot.subplot(2, 1, 2)
    pyplot.hist(x, bins=20)
    pyplot.xlabel('Track Duration')
    pyplot.ylabel("Count")

    pyplot.show()




if __name__ == "__main__":
    main()
    #   python playlist.py common pl1.xml pl2.xml
    #   python playlist.py plot rating.xml
