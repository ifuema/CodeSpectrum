import requests
import pandas as pd
import time
from openpyxl import load_workbook
import re
import difflib

# 单选/判断/多选
type = '单选'
# 文件
file = 'D:/maogai.xlsx'

answer = []
headers = {
    'Content-type': 'application/x-www-form-urlencoded',
}
pd.set_option('display.max_rows', None)
df = pd.read_excel(file, header=None, sheet_name=type)
for row in df.index:
    if str(df[0][row]).isdigit():
        time.sleep(1.5)
        # 接口1
        url1 = 'http://api.muketool.com/v1/cx'
        data1 = {
            'question': str(df[1][row]),
            'script': 'v1cx'
        }
        # 接口2
        url2 = 'http://cx.icodef.com/wyn-nb?v=3'
        data2 = {
            'question': re.sub('[()（）。.:： ]', '', str(df[1][row])),
        }

        # 判断
        if type == '判断':
            r2 = requests.post(url2, headers=headers, data=data2)
            if r2.json()['data'] == '正确':
                print('题目：' + data2['question'])
                print('答案：正确')
                answer.append('√')
            elif r2.json()['data'] == '错误':
                print('题目：' + data2['question'])
                print('答案：错误')
                answer.append('×')
            else:
                r1 = requests.post(url1, headers=headers, data=data1)
                if r1.json()['data'] in ['正确', '对', '√', '正确答案']:
                    print('题目：' + data1['question'])
                    print('答案：正确')
                    answer.append('√')
                elif r1.json()['data'] in ['错误', '错', '×', '错误答案']:
                    print('题目：' + data1['question'])
                    print('答案：错误')
                    answer.append('×')
                else:
                    answer.append('')
        # 单选/多选
        if type in ['单选', '多选']:
            r2 = requests.post(url2, headers=headers, data=data2)
            text = set()
            context = []
            print('题目：' + data2['question'])
            print('答案：' + r2.json()['data'])
            for i in range(row+1, df.index.stop):
                if str(df[0][i]).isdigit():
                    if type == '单选':
                        msg = [str(r2.json()['data'])]
                    elif type == '多选':
                        msg = str(r2.json()['data']).split('#')
                    for tab in msg:
                        tab = difflib.get_close_matches(tab, context, 1, cutoff=0.5)
                        if not tab:
                            tab = ''
                        else:
                            tab = tab[0]
                        if tab in context:
                            text.add(re.sub('[()（）。.:： ]', '', str(df[0][row + 1 + context.index(tab)])))
                    if not text:
                        print('' + '\n')
                        answer.append('')
                    else:
                        print('选项：' + str(text) + '\n')
                        answer.append(str(text))
                    for j in range(len(context)):
                        answer.append('')
                    break
                else:
                    print(str(df[0][i]) + ' ' + str(df[1][i]))
                    context.append(str(df[1][i]))
                    if i == df.index.stop-1:
                        if type == '单选':
                            msg = [str(r2.json()['data'])]
                        elif type == '多选':
                            msg = str(r2.json()['data']).split('#')
                        for tab in msg:
                            tab = difflib.get_close_matches(tab, context, 1, cutoff=0.5)
                            if not tab:
                                tab = ''
                            else:
                                tab = tab[0]
                            if tab in context:
                                text.add(re.sub('[()（）。.:： ]', '', str(df[0][row + 1 + context.index(tab)])))
                        if not text:
                            print('' + '\n')
                            answer.append('')
                        else:
                            print('选项：' + str(text) + '\n')
                            answer.append(str(text))
                        for j in range(len(context)):
                            answer.append('')

df[2] = answer
book = load_workbook(file)
with pd.ExcelWriter(file, engine='openpyxl') as writer:
    book.remove(book[type])
    writer.book = book
    df.to_excel(writer, index=False, header=None, sheet_name=type)
