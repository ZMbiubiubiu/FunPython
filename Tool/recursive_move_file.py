import os
import shutil

def out_file_from_dir(dir):
    for item in os.listdir(dir):
        path = os.path.join(dir, item)
        if os.path.isfile(path):
            print(path)
            try:
                shutil.move(path, '/home/bingo/文档/C++/例题与实验代码/CPPV4例题/')
            except:
                pass
#             os.system(f'mv {path} ')
        else:
            out_file_from_dir(path)