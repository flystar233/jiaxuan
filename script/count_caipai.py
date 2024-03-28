import pandas as pd
import re

# 读取csv文件
df = pd.read_csv('../data/cipai.csv')  # 将'filename.csv'替换为你的文件名

# 提取第二列的数据
data = df.iloc[:, 1]

# 计算第二列的中仄平一共加起来多少字
df['中'] = data.str.count('中')
df['平'] = data.str.count('平')
df['仄'] = data.str.count('仄')
df['总数'] = df['中'] + df['平'] + df['仄']

# 去掉『』（增韵）这些信息
data = data.replace(['『', '』', 'ˇ', '〖', '〗', '（增韵）'], '', regex=True)

# 以，。 、分割文本每段的字数
df['分段字数'] = data.apply(lambda x: [len(i) for i in re.split('，|。|、',x) if i])


df.to_csv('output.csv', index=False)