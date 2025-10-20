import os
import shutil

def copy_static(src: str, dst: str):
    if not os.path.exists(src):
        raise Exception("Source directory does not exist")
    
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)

    dir_list = os.listdir(src)

    for dir in dir_list:
        dst_path = os.path.join(dst, dir)
        src_path = os.path.join(src, dir)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
        else:
            copy_static(src_path, dst_path)
