import json
import pandas as pd

# 读取json文件
with open('新韵.json', 'r', encoding='utf-8') as f:
    pingshuiyun = json.load(f)

# 读取csv文件
df = pd.read_csv('cipai.csv')

# 输入的词
ci = '燕子几曾归去。只在翠岩深处。重到画梁间，谁与旧巢为主。深许。深许。闻道凤凰来住。'

# 判断输入的词的平仄
def judge_pingze(word):
    for group in pingshuiyun:
        for group_name, group_content in group.items():
            if word in group_content['平']:
                return '平'
            elif word in group_content['仄']:
                return '仄'
    return None

# 判断输入的词的词牌名
def judge_cipaiming(ci):
    ci_pingze = [judge_pingze(word) for word in ci]
    ci_pingze_str = ''.join([p if p else '中' for p in ci_pingze])
    for index, row in df.iterrows():
        if ci_pingze_str in row['韵律']:
            return row['词牌名']
    return None

cipaiming = judge_cipaiming(ci)
print(cipaiming)