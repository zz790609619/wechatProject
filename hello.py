from __future__ import unicode_literals
from wxpy import *
import requests
import json
import re
import urllib.request  #urllib2
import threading
import glob
import random
import urllib
import sys
import ssl
import base64
import os
from apscheduler.schedulers.blocking import BlockingScheduler
bot = Bot(cache_path=True)


def get_news():
    """获取金山词霸每日一句，英文和翻译"""
    url = "http://open.iciba.com/dsapi/"
    r = requests.get(url)
    content = r.json()['content']
    note = r.json()['note']
    return content, note


def send_news(info):
    try:
        contents = get_news()
        # 你朋友的微信名称，不是备注，也不是微信帐号。
        # my_friend = bot.friends().search(u'M_M')[0]
        # my_friend.send(contents[0])
        # my_friend.send(contents[1])
        # my_friend.send(u"晚安")
        # 微信公众号
        aoti =bot.mps().search('adidasOriginals')[0]
        aoti.send(info)
    except:
        # 你的微信名称，不是微信帐号。
        my_friend = bot.friends().search('我小叮当无可奈何')[0]
        my_friend.send(u"今天消息发送失败了")


@bot.register(except_self=False)
def print_others(msg):
    print(msg)
    message = msg.text
    type = msg.type
    reply = u''
    if type == 'Text':
        # adidas微信公众号抽签
        if u'已结束' in message:
            reply = u"谢谢"
            return reply
        elif u'感谢您参与' in message:
            cmdm = message.find('尺码代码')
            sfz = message.find('身份证')
            sjh = message.find('手机号')
            sfzNum = '320324199608134190'
            sjhNum = '18550857425'
            cmdmNum = '7.5'
            if cmdm == -1:
                if sfz < sjh:
                    reply = sfzNum+u'，'+sjhNum
                else:
                    reply = sjhNum+u'，'+sfzNum
            else:
                if cmdm < sfz < sjh:
                    reply = cmdmNum+u','+sfzNum+u'，'+sjhNum
                elif cmdm < sjh < sfz:
                    reply = cmdmNum+u','+sjhNum+u'，'+sfzNum
                elif sjh < cmdm < sfz:
                    reply = sjhNum+u','+cmdmNum+u'，'+sfzNum
                elif sjh < sfz < cmdm:
                    reply = sjhNum+u','+sfzNum+u'，'+cmdmNum
                elif sfz < sjh < cmdm:
                    reply = sfzNum+u'，'+sjhNum+u'，'+cmdmNum
                elif sfz < cmdm < sjh:
                    reply = sfzNum+u'，'+cmdmNum+u'，'+sjhNum
            return reply
        else:
            # 机器人自动陪聊
            if get_response(message) != '亲爱的，当天请求次数已用完。':
                reply = get_response(message)
            else:
                reply = ''
            return reply
    elif type == 'Picture':
        # 识别图中文字
        # path = os.path.join('./getImages/' + msg.file_name)
        # msg.get_file(path)
        # getMessageByImage(msg.file_name)
        # 自动回复表情包
        searchImg('')
        i = random.randint(1, 50)
        msg.reply_image(imgs[i])
        imgs.clear()
        for img in imgs[:3]:
            msg.reply_image(img)
            print('开始发送表情：', img)
            imgs.clear()
        return reply


# 识别图片文字
def getMessageByImage(imageName):
    takonUrl = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=s0IvNnpvHF2F89tdsw2Gcwtm&client_secret=jYQ1vsozTEmz9qfObtrsWA7WNTVvLZcs'
    res = requests.get(takonUrl)
    takon = res.json()['access_token']
    url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general?access_token=' + takon
    with open(current_path+'/getImages/'+imageName, 'rb') as f:
        data = base64.b64encode(f.read())
    imageEncode = str(data, 'utf-8')
    params = {"image": imageEncode}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    postdata = urllib.parse.urlencode(params).encode('utf-8')
    request = urllib.request.Request(url=url, data=postdata, headers=headers)
    res = urllib.request.urlopen(request)
    page_source = res.read().decode('utf-8')


def get_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'   #图灵机器人的api
    payload = {
        'key': 'ce697b3fc8b54d5f88c2fa59772cb2cf',  # api Key
        'info': msg,  # 这是我们收到的消息
        'userid': 'wechat-robot',  # 这里可随意修改
    }
    # 通过如下命令发送一个post请求
    r = requests.post(apiUrl, data=json.dumps(payload))
    mes = json.loads(r.text)['text']
    return mes


# 获取表情包
def Downloader(step):
    # 定义目标网站url
    baseurl = 'http://www.doutula.com/photo/list/?page='
    # #编写模拟浏览器获取
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'gzip',
        'Connection': 'close',
        'Referer': None  # 注意如果依然不能抓取的话，这里可以设置抓取网站的host
        }
    # 遍历获得目标网站的每一页

    a = step * 50
    b = step * 50 + 50
    for i in range(a, b):
        urls = baseurl + str(i)
        print(urls)

        # 用Request的get请求获取网页代码
        r = requests.get(urls, headers=headers)
        html = r.text
        # #用正则匹配获取图片链接
        zz = re.compile(r'data-original="(.*?)".*?alt="(.*?)"', re.S)
        img = re.findall(zz, html)
        # 遍历得到图片名字和url
        for a in img:
            # 设置保存路径
            imgname = a[1]
            imgname = re.sub('\/|\\\\|《|》|。|？|！|\.|\?|!|\*|&|#|(|)|(|)|（|）', '', imgname)
            imgtype = a[0].split('.')[-1]
            path = ('battleImages/%s.%s' % (imgname, imgtype))
            print(path, a[0])
            # 用urllib库来进行保存
            dir = os.path.join('./', path)
            urllib.request.urlretrieve(a[0], dir)


t_obj = []
# 多线程爬取表情包
for i in range(10):
    t = threading.Thread(target=Downloader, args=(i,))
    # t.start()
    # t_obj.append(t)

for t in t_obj:
    t.join()


current_path = os.getcwd()
imgs=[]

# 寻找图
def searchImg(keywords):
    print('keywords: %s' % keywords)
    for name in glob.glob(current_path+'/battleImages/*'+keywords+'.*'):
        imgs.append(name)


if __name__ == "__main__":
    scheduler = BlockingScheduler()
    # 间隔3秒钟执行一次
    scheduler.add_job(func=send_news, trigger='cron', hour='13', minute='0', second='0', args=['YEEZY苏州'])
    # 这里的调度任务是独立的一个线程
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
