此库专门存储辛弃疾(稼轩)的诗词，并确定了每一首的唯一性和准确性。补全了网上很多由于编码问题存在□的问题。
## 已做事项
1. 寻找文献补全诗词
2. 诗词去重
3. 同义词牌名合并
4. 分析词频
5. 整理词牌名平仄
6. 增加评估新词功能
## 待做事项
## 使用方法
从网站爬取词牌名相关信息
```sh
python get_cipai.py
```
对词牌名信息进行统计
```sh
python statistic_caipai.py
```
对诗词进行词牌名使用频率统计
```sh
python plot_frequency.py
```
评估新词评估新词
```sh
python estimate_poetry.py
```
## 词牌名使用频率
<p align="center">
    <img src="image/frequency.png" width="247.5",height="300"/><img src="image/bar.png" width="500",height="300"/>
</p>

## 词频分析
<p align="center">
    <img src="image/echarts.png" width="750"/>
</p>
