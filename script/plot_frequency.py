from pyecharts.charts import Pie
from pyecharts.charts import Bar
from pyecharts import options as opts
import pandas as pd

# 读取数据
df = pd.read_csv('../jiaxuan_poetry.csv')
categories =['浪淘沙', '感皇恩', '新荷叶', '满庭芳', '瑞鹤仙', '瑞鹧鸪', '蓦山溪', '鹊桥仙', '踏莎行', '踏歌', '醉太平', '醉翁操', '鹧鸪天', '唐多令', '霜天晓角',\
 '一枝花', '一络索', '一落索', '千秋岁', '东坡引', '阮郎归', '破阵子', '哨遍', '品令', '惜奴娇', '眼儿媚', '绿头鸭', '谒金门', '喜迁莺', '御街行', '最高楼', '朝中措', \
 '六么令', '六州歌头', '太常引', '水调歌头', '兰陵王', '归朝欢', '永遇乐', '玉蝴蝶', '杏花天', '苏武慢', '夜游宫', '定风波', '汉宫春', '武陵春', '河渎神', '采桑子', \
 '雨中花慢', '南歌子', '柳梢青', '洞仙歌', '祝英台近', '贺新郎', '浣溪沙', '恋绣衾', '粉蝶儿', '酒泉子', '减字木兰花', '婆罗门引', '惜分飞', '昭君怨', '玉楼春', '生查子',\
  '好事近', '行香子', '木兰花慢', '渔家傲', '青玉案', '满江红', '如梦令', '醉花阴', '虞美人', '水龙吟', '卜算子', '菩萨蛮', '临江仙', '江城子', '蝶恋花', '凤凰台上忆吹箫', \
  '念奴娇', '西江月', '南乡子', '暗香', '摸鱼儿', '沁园春', '长相思', '声声慢', '点绛唇', '清平乐', '瑞龙吟', '一剪梅', '千年调', '丑奴儿', '八声甘州', '小重山', '上西平', '乌夜啼']

result = {}
for category in categories:
    result[category] = df[df['title'].str.contains(category)].shape[0]

result_filter_for_pie= [(kay,value) for kay,value in result.items() if value>=10]
result_sorted_for_pie = sorted(result_filter_for_pie,key=lambda x: x[1], reverse=True)
result_filter_for_bar= [(kay,value) for kay,value in result.items() if value>=1]
result_sorted_for_bar = sorted(result_filter_for_bar,key=lambda x: x[1], reverse=True)

categories_pie = [item[0] for item in result_sorted_for_pie]
counts_pie = [item[1] for item in result_sorted_for_pie]
categories_bar = [item[0] for item in result_sorted_for_bar]
counts_bar = [item[1] for item in result_sorted_for_bar]

pie = Pie(init_opts=opts.InitOpts(width='800px', height='800px')) 

# 添加数据，设置类别名为图例，使用"radius"模式创建南丁格尔玫瑰图
pie.add("", [list(z) for z in zip(categories_pie, counts_pie)], radius=["40%", "110%"], center=["50%", "60%"], rosetype="radius")

# 设置全局配置项
pie.set_global_opts(title_opts=opts.TitleOpts(title="pie"), legend_opts=opts.LegendOpts(is_show=False))

# 设置系列配置项
pie.set_series_opts(label_opts=opts.LabelOpts(is_show=True, position="inside", font_size=12, formatter="{b}:{c}", font_style="italic", font_weight="bold", font_family="Microsoft YaHei"))

# 生成html文件
pie.render("pie.html")


bar = Bar(init_opts=opts.InitOpts(width='2000px', height='800px'))  # 设置画布大小

# 添加数据，设置类别名为图例
bar.add_xaxis(categories_bar)
bar.add_yaxis("", counts_bar,bar_width="90%")
#bar.reversal_axis()

# 设置全局配置项
bar.set_global_opts(title_opts=opts.TitleOpts(title="bar"), 
                    legend_opts=opts.LegendOpts(is_show=False),
                    visualmap_opts=opts.VisualMapOpts(max_=max(counts_bar), range_color=['#FFF5A5','#FFA500']),
                    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=90)))

# 设置系列配置项
bar.set_series_opts(label_opts=opts.LabelOpts(is_show=False))

# 生成html文件
bar.render("bar.html")


