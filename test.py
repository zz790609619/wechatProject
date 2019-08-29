# encoding: utf-8
# 5.获取好友微信名称，词云分析
from wxpy import *
from os import path
import re
import os
import sys
# 清洗数据，生成词云图
#获取当前的项目文件加的路径
d=path.dirname(__file__)
#读取停用词表
stopwords_path=d + '/static/stopwords.txt'


# 获取文件所在的绝对路径
def get_dir(sys_arg):
    sys_arg = sys_arg.split("/")
    dir_str = ""
    count = 0
    for cur_dir in sys_arg:
        if count == 0:
            count = count + 1
        if count == len(sys_arg):
            break
        dir_str = dir_str + cur_dir + "/"
        count = count + 1
    return dir_str


if __name__=='__main__':

    # 获取当前路径信息
    curr_dir = get_dir(sys.argv[0])
    # 如果FriendImgs目录不存在就创建一个
    if not os.path.exists(curr_dir + "FriendImgs/"):
        os.mkdir(curr_dir + "FriendImgs/")

    # 登录微信并获取好友信息
    bot = Bot(cache_path=False)
    #获取好友列表(包括自己)
    my_friends = bot.friends(update=True)
    # 微信昵称
    nick_name = ''
    # 微信个性签名
    wx_signature = ''
    alls = ''
    for friend in my_friends:
        # 微信昵称：NickName
        nick_name = nick_name + friend.raw['NickName']+': '+friend.raw['Signature']+'\n'
        print(nick_name)
