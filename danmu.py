import websocket
import time
import msgpack
import html
import pymysql

"""
    接收弹幕并处理
"""
conn = None
cursor = None
read_flag = True  # 控制是否输出弹幕信息
write_flag = True  # 控制是否将弹幕信息存入数据库


def get_danmu_from_longzhu():
    ws = websocket.WebSocket()
    url = 'ws://idc-bgp-zs.longzhu.com:8805/?room_id=2241164&msgpack=1&connType=1'
    ws.connect(url)
    while True:
        tmp = ws.recv()
        text = msgpack.unpackb(tmp, encoding='utf-8')
        if isinstance(text, dict):
            parse_data(text)
        if isinstance(text, list):
            for information in text:
                parse_data(information)


def parse_data(information):
    """
    解析从服务器发来的数据，根据read_flag和write_flag决定输出和写入
    :param information:从服务器发来的数据
    """
    _type = information['type']  # 只记录类型为‘chat’的信息
    if 'chat' != _type:
        return
    msg = information['msg']

    medal = None  # 粉丝牌
    name = None  # 粉丝牌名字
    level = None  # 粉丝牌等级
    if 'medal' in msg:
        medal = msg['medal']
        name = medal['name']
        level = int(medal['level'])
    _time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(msg['time'][6:16])))  # 用户发言时间
    user = msg['user']  # 用户信息
    content = html.unescape(msg['content'])  # 弹幕内容
    via = msg['via']  # 观看直播的方式 1.0为PC,2.0为安卓,3.0为苹果
    methods = ['PC', '安卓', '苹果', '未知设备']
    if int(via) in [1, 2, 3]:
        via = methods[int(via) - 1]
    else:
        via = methods[3]
        print('!' * 20, end='')
        with open('./error.log', 'a') as f:
            f.write('Unknown devices!' + '\n')  # 提示有未知设备出现，该更新代码了

    uid = int(user['uid'])  # 龙珠号
    username = user['username']  # 用户名
    grade = int(user['newGrade'])  # 用户当前等级
    if read_flag:
        if medal and name == '德云色':
            print('【%s】%s:%s' % (grade, username, content))
        else:
            print('[%s]%s:%s' % (grade, username, content))
    if write_flag:
        sql = "insert into danmu values(null,%s,%s,%s,%s,%s,%s,%s,%s)"
        args = (uid, username, content, grade, _time, via, name, level)
        insert_database(sql, args)


def insert_database(sql, args):
    """
    将弹幕信息写入数据库
    :param sql: SQL语句
    :param args: SQL参数
    """
    try:
        cursor.execute(sql, args)
        conn.commit()
    except Exception as e:
        print(e)
        print('Error!Got incorrect characters!')
        with open('./error.log', 'a') as f:
            f.write(str(e) + '\n')
        conn.rollback()


def main():
    global conn, cursor
    if not (read_flag | write_flag):  # 如果既不读弹幕信息，又不写弹幕信息，执行该程序没有意义
        exit(1)
    if write_flag:
        try:
            conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', database='longzhu',
                                   charset='utf8mb4')
            cursor = conn.cursor()
        except Exception:
            print('数据库连接失败!')
            exit(1)
    try:
        get_danmu_from_longzhu()
    except Exception as e:
        print(e)
        print('Main function error')
    finally:
        if write_flag:
            cursor.close()
            conn.close()


if __name__ == '__main__':
    main()
