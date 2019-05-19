# print_directory_content.py
# Created: 5 10 2019

"""
    递归打印给定目录下所有的文件
"""

import os
def print_directory_content(dir):
    for file in os.listdir(dir):
        file_path = os.path.join(dir, file)
        if os.path.isdir(file_path):
            print_directory_content(file_path)
        else:
            print(file_path)

if __name__ == "__main__":
    print_directory_content('/home/bingo/Test')