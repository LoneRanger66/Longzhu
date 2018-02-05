import requests
import json
from contextlib import closing
import time
import threading


class RecordVideo:
    def __init__(self, name, chunk_size):
        self.file = name
        self.url = 'http://livestream.plu.cn/live/getlivePlayurl?roomId=2241164&v2'  # 目前龙珠的API，不能更改
        self.chunk_size = chunk_size
        self.count = 0  # 当前文件大小

    def get_url(self):
        while True:  # 请求直播地址。如果未直播，则循环请求，直到成功
            try:
                response = requests.get(self.url)
            except KeyboardInterrupt:
                print('手动结束程序')
            except Exception as e:
                print(e)
            data = json.loads(response.text)
            if data['playLines']:
                break
            time.sleep(5)  # 5秒后继续请求
        try:
            for i in data['playLines'][0]['urls']:
                if i['rateLevel'] == 5 and i['ext'] == 'flv':  # 选择清晰度最高的视频来录制
                    self.url = i['securityUrl']
                    print('视频地址：' + self.url)
        except Exception as e:
            print(e)
            print('json格式错误！')

    def record_video(self):
        try:
            with open(self.file, 'wb') as f:
                with closing(requests.get(self.url, stream=True)) as response:
                    print('正在存储直播视频......')
                    for chunk in response.iter_content(chunk_size=self.chunk_size):
                        if chunk:
                            f.write(chunk)
                            self.count += 1
        except KeyboardInterrupt:
            print('手动结束程序')
        except Exception as e:
            print(e)

    def show_file_size(self, frequent):
        while True:
            size = self.count * self.chunk_size  # 单位：B
            print('文件大小：%sMB' % str(size / 1024 / 1024))
            time.sleep(frequent)


def main():
    name = './video.flv'  # 存储视频的绝对路径，自己更改
    chunk_size = 1024 * 1024 * 1  # 每1MB存储一次
    frequent = 1  # 控制显示文件大小的时间频率（秒）
    task = RecordVideo(name, chunk_size)
    t = threading.Thread(target=task.show_file_size, args=(frequent,), daemon=True)
    t.start()
    task.get_url()
    task.record_video()


if __name__ == '__main__':
    main()
