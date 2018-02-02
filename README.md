# Longzhu
抓取龙珠（德云色房间）的弹幕，并存入数据库，分析弹幕数据

python版本：python3.6.4
danmu.py
    使用时，设置参数read_flag和write_flag，控制是否输出弹幕信息和是否将弹幕信息存入数据库。
dbhelper.py
    数据库连接辅助类，用来从数据库中获取信息
paint.py
    用于生成图表。使用时，可以通过更改__init__(self)函数中的self.prefix来更改存储图片的位置

依赖包：requirements.txt,可以通过命令pip install -r requirements.txt安装