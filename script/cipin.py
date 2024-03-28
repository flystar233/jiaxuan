import pandas as pd
import jieba
import re
from collections import Counter

# 读取CSV文件
df = pd.read_csv('../jiaxuan_poetry.csv')  # 请将'yourfile.csv'替换为你的CSV文件路径
words = []
for content in df['content']:
    content = re.sub(r'\t|\n|\.|-|:|;|\)|\(|\?|"|。|，|、', '', content)
    words.extend(jieba.cut(content))

# 进行词频分析
word_counts = Counter(words)
top_20_words = word_counts.most_common(20)
# 打印词频分析结果
print(top_20_words)