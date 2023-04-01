# 父文件
filename1 = ''
# 被去重文件
filename2 = ''
# 去重后新文件
filename3 = ''
str1 = []
str_dump = []
with open(filename1, "r", encoding="utf-8") as f:
    for line in f.readlines():
        str1.append(line)
with open(filename2, "r", encoding="utf-8") as f:
    for line in f.readlines():
        if line not in str1:
            str_dump.append(line)
with open(filename3, "w", encoding="utf-8") as f:
    for line in str_dump:
        f.write(line)
