import dbhelper
import matplotlib.pyplot as plt


class Paint:
    """
    根据数据库中的数据来画以下图：
    用户设备的分布图（饼图）、所有弹幕的设备分布图（饼图）、发弹幕用户中的粉丝比例（饼图）、弹幕条数走势图（折线图）
    计算每个用户弹幕数的平均值
    """
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 为了在图中显示中文

    def __init__(self):
        self.data = dbhelper.Data()
        self.prefix = 'E:/'  # 存储图片的位置
        self.suffix = '.png'  # 存储图片的类型

    def get_user_devices(self):
        """ 用户设备的分布图（饼图）"""
        count, label = self.data.get_user_devices()
        plt.figure(1)
        plt.pie(count, labels=label, startangle=90, autopct='%1.1f%%')
        title = '用户设备分布'
        plt.title(title)
        plt.legend(bbox_to_anchor=(0.9, 0.95))
        plt.savefig(self.prefix + title + self.suffix)

    def get_danmu_devices(self):
        """所有弹幕的设备分布图（饼图）"""
        count, label = self.data.get_danmu_devices()
        plt.figure(2)
        plt.pie(count, labels=label, startangle=90, autopct='%1.1f%%')
        title = '所有弹幕中的设备分布'
        plt.title(title)
        plt.legend(bbox_to_anchor=(0.9, 0.95))
        plt.savefig(self.prefix + title + self.suffix)

    def get_fans(self):
        """发弹幕用户中的粉丝比例（饼图）"""
        count, label = self.data.get_fans()
        plt.figure(3)
        plt.pie(count, labels=label, startangle=90, autopct='%1.1f%%')
        title = '所有弹幕中的粉丝分布'
        plt.title(title)
        plt.legend(bbox_to_anchor=(0.8, 0.9))
        plt.savefig(self.prefix + title + self.suffix)

    def get_danmu_per_hour(self, start_year, start_month, start_day, start_hour, end_year, end_month, end_day,
                           end_hour):
        """弹幕条数走势图（折线图）"""
        count, label = self.data.get_danmu_per_hour(start_year, start_month, start_day, start_hour, end_year, end_month,
                                                    end_day,
                                                    end_hour)
        plt.figure(4)
        title = '弹幕条数走势图'
        plt.title(title)
        plt.xticks(range(0, len(label), int(len(label) / 30)),
                   (label[x] for x in range(0, len(label), int(len(label) / 30))), rotation=90)
        plt.plot(label, count)
        plt.xlabel('时间')
        plt.ylabel('弹幕数量')
        plt.savefig(self.prefix + title + self.suffix)


def main():
    paint = Paint()
    paint.get_user_devices()
    paint.get_danmu_devices()
    paint.get_fans()
    paint.get_danmu_per_hour(2018, 2, 1, 18, 2018, 2, 2, 6)
    data = dbhelper.Data()
    print('平均每个用户发送弹幕条数：' + str(data.get_danmu_per_user()))


if __name__ == '__main__':
    main()
