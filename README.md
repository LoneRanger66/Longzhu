# Longzhu
一些龙珠（德云色房间）的实用小工具，目前有以下功能：
抓取房间弹幕，并存入数据库，分析弹幕数据；
得到德云色房间的直播地址；
录制德云色房间的直播视频。

python版本：python3.6.4

danmu.py：使用时，设置参数read_flag和write_flag，控制是否输出弹幕信息和是否将弹幕信息存入数据库。

dbhelper.py：数据库连接辅助类，用来从数据库中获取信息

paint.py：用于生成图表。使用时，可以通过更改__init__(self)函数中的self.prefix来更改存储图片的位置

get_dys_url.py：用于得到德云色房间的直播地址，并将地址存入当前文件夹下。得到直播地址后，可以使用PotPlayer等视频软件打开观看直播

record_video.py：用于录制德云色房间的直播视频

依赖包：requirements.txt,可以通过命令pip install -r requirements.txt安装

download文件夹下，danmu.exe用来观看弹幕，get_dys_url.exe用来得到直播地址。（小白用户使用，兼容性未知）