import os
import hashlib
from tqdm import tqdm

def calculate_hash(file_path, hash_algorithms):
    total_size = os.path.getsize(file_path)
    progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

    # 初始化哈希算法字典
    hashes = {name: hashlib.new(name) for name in hash_algorithms}

    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            for hash_name, hash_obj in hashes.items():
                hash_obj.update(chunk)
            progress_bar.update(len(chunk))
    
    progress_bar.close()

    # 返回计算后的哈希值
    return {name: hash_obj.hexdigest() for name, hash_obj in hashes.items()}

def calculate_hash_for_folder(folder_path, hash_algorithms):
    total_size = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            total_size += os.path.getsize(file_path)

    progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)
    
    # 初始化哈希算法字典
    hashes = {name: hashlib.new(name) for name in hash_algorithms}

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    for hash_name, hash_obj in hashes.items():
                        hash_obj.update(chunk)
                    progress_bar.update(len(chunk))
    
    progress_bar.close()

    # 返回计算后的哈希值
    return {name: hash_obj.hexdigest() for name, hash_obj in hashes.items()}

def main():
    while True:
        path = input("请输入文件或文件夹地址：")
        if os.path.isfile(path):
            print(f"计算文件 {path} 的哈希值：")
            hash_values = calculate_hash(path, ["md5", "sha256"])
            print("MD5值:", hash_values["md5"])
            print("SHA-256值:", hash_values["sha256"])
        elif os.path.isdir(path):
            print(f"计算文件夹 {path} 的哈希值：")
            hash_values = calculate_hash_for_folder(path, ["md5", "sha256"])
            print("MD5值:", hash_values["md5"])
            print("SHA-256值:", hash_values["sha256"])
        else:
            print("输入的不是有效的文件或文件夹地址。")

if __name__ == "__main__":
    main()
