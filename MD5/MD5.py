import os
import hashlib
from tqdm import tqdm

def calculate_md5(file_path):
    md5 = hashlib.md5()
    total_size = os.path.getsize(file_path)
    progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5.update(chunk)
            progress_bar.update(len(chunk))
    progress_bar.close()

    return md5.hexdigest()

def calculate_md5_for_folder(folder_path):
    md5 = hashlib.md5()
    total_size = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            total_size += os.path.getsize(file_path)

    progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    md5.update(chunk)
                    progress_bar.update(len(chunk))
    progress_bar.close()

    return md5.hexdigest()

def main():
    while True:
        path = input("请输入文件或文件夹地址：")
        if os.path.isfile(path):
            file_md5 = calculate_md5(path)
            print("文件的MD5值:", file_md5)
        elif os.path.isdir(path):
            folder_md5 = calculate_md5_for_folder(path)
            print("文件夹的MD5值:", folder_md5)
        else:
            print("输入的不是有效的文件或文件夹地址。")

if __name__ == "__main__":
    main()
