import requests
import json


def get_url_and_save():
    """得到德云色房间的直播地址，并将地址存到当前文件夹下"""
    url = 'http://livestream.plu.cn/live/getlivePlayurl?roomId=2241164&v2'  # 目前龙珠的API，不能更改
    response = requests.get(url)
    data = json.loads(response.text)
    if not data['playLines']:
        print('主播未直播！')
        exit(1)
    rate_level = ['普清', '高清', '超清', '蓝光']  # 在返回的数据中分别是2、3、4、5
    f = open('./直播地址.txt', 'w', encoding='utf-8')
    try:
        for i in data['playLines'][0]['urls']:
            print(i)
            model = dict()
            model['清晰度'] = rate_level[i['rateLevel'] - 2]
            model['直播地址'] = i['securityUrl']
            model['分辨率'] = i['resolution']
            model['类型'] = i['ext']
            result = json.dumps(model, ensure_ascii=False)
            f.write(result + '\n')
    except Exception as e:
        print(e)
        print('json格式错误！')
    f.close()
    print('成功获取直播地址！')


if __name__ == '__main__':
    get_url_and_save()
