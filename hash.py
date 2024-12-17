import os
import hashlib
import sys
from tqdm import tqdm

def calculate_hash(file_path, hash_algorithm):
    total_size = os.path.getsize(file_path)
    progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

    # 根据传入的算法名称创建哈希对象
    hash_obj = hashlib.new(hash_algorithm)

    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_obj.update(chunk)
            progress_bar.update(len(chunk))
    
    progress_bar.close()

    # 返回计算后的哈希值
    return hash_obj.hexdigest()

def calculate_hash_for_folder(folder_path, hash_algorithm):
    total_size = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            total_size += os.path.getsize(file_path)

    progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

    # 根据传入的算法名称创建哈希对象
    hash_obj = hashlib.new(hash_algorithm)

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_obj.update(chunk)
                    progress_bar.update(len(chunk))
    
    progress_bar.close()

    # 返回计算后的哈希值
    return hash_obj.hexdigest()

def main():
    if len(sys.argv) != 2:
        print("请传入哈希类型（md5 或 sha256）作为参数！")
        sys.exit(1)

    hash_algorithm = sys.argv[1].lower()
    
    if hash_algorithm not in ["md5", "sha256"]:
        print("无效的哈希类型，支持的类型是：md5 或 sha256。")
        sys.exit(1)

    while True:
        path = input("请输入文件或文件夹地址：")
        if os.path.isfile(path):
            print(f"计算文件 {path} 的 {hash_algorithm.upper()} 哈希值：")
            hash_value = calculate_hash(path, hash_algorithm)
            print(f"{hash_algorithm.upper()}值:", hash_value)
        elif os.path.isdir(path):
            print(f"计算文件夹 {path} 的 {hash_algorithm.upper()} 哈希值：")
            hash_value = calculate_hash_for_folder(path, hash_algorithm)
            print(f"{hash_algorithm.upper()}值:", hash_value)
        else:
            print("输入的不是有效的文件或文件夹地址。")

if __name__ == "__main__":
    main()