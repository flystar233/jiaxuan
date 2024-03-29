import json
import pandas as pd
import re

# 读取json文件
with open('../data/新韵.json', 'r', encoding='utf-8') as f:
    xinyun = json.load(f)


# 读取csv文件
df = pd.read_csv('../data/cipai_with_statistics.csv')

# 输入的词

def estimate_poetry(text):
    text_drop = re.sub("[^\u4e00-\u9fa5]", "", text)
    length = len(text_drop)
    split_length = [len(i) for i in re.split('，|。|、',text) if i]
    guess_cipai='未查到词牌名'
    pingze_database = []
    for index, cipai in df.iterrows():
        if length == cipai['总数'] and str(split_length) == cipai['分段字数']:
            guess_cipai = cipai['词牌名']
            pingze_database = cipai['韵律']

    pingze_database=  list(re.sub("[^\u4e00-\u9fa5]", "", pingze_database))

    pingze_text = []
    for word in text_drop:
        for item in xinyun:
            for key, value in item.items():
                if word in value['平']:
                    pingze_text.append((word,'平'))
                    break
                elif word in value['仄']:
                    pingze_text.append((word,'仄'))
                    break
            else:
                continue
            break

    score = 0
    for item1, item2 in zip(pingze_text,pingze_database):
        if item1[1]!=item2 and item2!='中':
            print(item1, item2)
        elif item1[1]==item2 or item2=='中':
            score+=1
    score= score/length*100
    return guess_cipai,score

text = "云气上林梢，毕竟非空非色。风景不随人去，到而今留得。老无情味到篇章，诗债怕人索。却笑近来林下，有许多词客。"
guess_cipai = estimate_poetry(text)
print(guess_cipai)