#! /home/bingo/anaconda3/bin/python
# *- coding=utf-8 -*

__author__ = "ZzLee"
__date__ = "2019/04/27"
__mail__ = "zhangmeng.lee@foxmail.com"
__version__ = "1.0"


import os
import click

# decorator
def ls_long(func):
    def wrapper(**kwargs):
        files, path = ls(**kwargs)
        for file in files:
            full_file = os.path.join(path, file)
            file_size = round(float(os.path.getsize(full_file)) / 1024, 2)
            file_type = None
            if os.path.isfile(full_file):
                file_type = 'f'
            elif os.path.isdir(full_file):
                file_type = 'd'
            elif os.path.islink(full_file):
                file_type = 'l'
            print(f'{file_type}  {file_size}k \t{file}')
    return wrapper

def ls_normal(func):
    def wrapper(**kwargs):
        files,_ = func(**kwargs)
        for file in files:
            print(file, end='\t')
        print('\n')
    return wrapper


def ls(path, all):
    files = []
    for file in os.listdir(path):
        if not all and file.startswith('.'):
            continue
        files.append(file)
    return files, path

lsn = ls_normal(ls)
lsl = ls_long(ls)

@click.command()
@click.option('--long-format', '-l', default=None,help="Use a long list formatting")    
@click.option('--all-detail', '-a', default=None,help="Oupt all files")  
@click.option('--file-path', '-p', default='.', help="The path you want to show")     
def main(long_format, all_detail, file_path):
    """
    Create a small 'ls' commond
    """
    if long_format:
        lsl(all=all_detail, path=file_path)
    else:
        lsn(all=all_detail, path=file_path)

if __name__ == "__main__":
    main()

# python ls.py -l 1 -a 1 -p /home/bingo/Test

