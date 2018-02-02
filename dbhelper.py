import pymysql


class Data:
    """

    """
    def __init__(self):
        """初始化conn和cursor"""
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', database='longzhu',
                                    charset='utf8mb4')
        self.cursor = self.conn.cursor()

    def get_user_devices(self):
        """
        得到用户的设备数量分布（PC、安卓、苹果）
        :return: 两个list，如[1000,1000,1000],['PC','安卓','苹果']
        """
        sql = 'select count(distinct(uid)),via from danmu group by via'
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        count = []
        devices = []
        for t in data:
            count.append(t[0])
            devices.append(t[1])
        return count, devices

    def get_danmu_devices(self):
        """
        得到弹幕的设备数量分布（PC、安卓、苹果）
        :return: 两个list，如[1000,1000,1000],['PC','安卓','苹果']
        """
        sql = 'select count(content),via from danmu group by via'
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        count = []
        devices = []
        for t in data:
            count.append(t[0])
            devices.append(t[1])
        return count, devices

    def get_fans(self):
        """
        得到戴各种粉丝牌的用户数量（德云色、无、其它）
        :return:tuple，（德云色粉丝数量，没有粉丝牌的数量，其它粉丝牌的数量）
        """
        sql = 'select name,count(distinct(uid)) from danmu group by name'
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        count = 0
        notfan_count = 0
        dys_count = 0
        for t in data:
            count += t[1]
            if not t[0]:
                notfan_count = t[1]
            elif t[0] == '德云色':
                dys_count = t[1]
        other_count = count - notfan_count - dys_count
        count_list = [dys_count, notfan_count, other_count]
        fan_list = ['德云色粉丝', '没有粉丝牌', '其它粉丝']
        return count_list, fan_list

    def get_danmu_per_hour(self, start_year, start_month, start_day, start_hour, end_year, end_month, end_day,
                           end_hour):
        """
        得到每小时的弹幕条数
        :param start_year: 开始的年份
        :param start_month: 开始的月份
        :param start_day: 开始的日期
        :param start_hour: 开始的小时
        :param end_year: 结束的年份
        :param end_month: 结束的月份
        :param end_day: 结束的日期
        :param end_hour: 结束的小时
        :return: 从18点到凌晨的弹幕数量count_list和相对应的小时数hour_list
        """
        sql = "select count,from_unixtime(stamp*600) from (select count(*) as count,FLOOR(UNIX_TIMESTAMP(time)/600) as stamp from danmu where time>=%s and time<=%s group by FLOOR(UNIX_TIMESTAMP(time)/600)) as a"
        start_time = '{}-{}-{} {}:00:00'.format(start_year, start_month, start_day, start_hour)
        end_time = '{}-{}-{} {}:00:00'.format(end_year, end_month, end_day, end_hour)
        args = (start_time, end_time)
        self.cursor.execute(sql, args)
        time_list = []
        count_list = []
        data = self.cursor.fetchall()
        for t in data:
            count_list.append(t[0])
            time_list.append(t[1].isoformat(sep=' ')[5:-3])
        return count_list, time_list

    def get_danmu_per_user(self):
        """得到平均每个用户发的弹幕数"""
        sql = 'select count(*) from danmu'
        self.cursor.execute(sql)
        danmu_all = self.cursor.fetchone()[0]
        sql = 'select count(distinct(uid)) from danmu'
        self.cursor.execute(sql)
        user_all = self.cursor.fetchone()[0]
        return round(danmu_all / user_all, 2)

    def get_user_content(self, uid):
        """
        根据用户的uid查询发言详情
        待实现
        130888609
        :param uid: 龙珠号
        :return:
        """
        sql = "select uid as '龙珠号',username as '用户名',content as '弹幕内容',grade as '用户等级',time as '发言时间',via as '设备' from danmu where uid=%s"
        pass

    def get_datetime(self):
        sql = 'select time from danmu where uid=%s'
        args = (1529517,)
        self.cursor.execute(sql, args)
        data = self.cursor.fetchall()
        print(len(data))
        if data:
            for a in data:
                print(a[0].isoformat(sep=' '))  # 取出datetime 标准化


def main():
    data = Data()
    data.get_user_devices()
    data.get_danmu_devices()
    data.get_fans()
    data.get_danmu_per_hour(2018, 2, 1, 18, 2018, 2, 2, 6)
    data.get_danmu_per_user()


if __name__ == '__main__':
    main()
