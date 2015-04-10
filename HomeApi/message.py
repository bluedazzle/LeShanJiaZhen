# -*- coding: utf-8 -*-
from HomeApi.models import *
import datetime


REG_MES = '恭喜您获得%s元维修基金'
INV_MES = '您的好友接受邀请，恭喜您获得%s元维修基金'
IN_MES = '恭喜您接受邀请，获得%s元维修基金'
GAME_MES = '恭喜您通过游戏获得%s元维修基金'
PAY_MES = '恭喜您通过在线支付获得%s元维修基金'
DIR_MES = '恭喜您获得系统赠送的%s元维修基金'
CANCEL_MES = '您的订单%s被取消，请到订单中心查看详情'
ACCEPT_MES = '您的订单%s已接受，请到订单中心查看详情'



def create_new_message(content, curuser, expire=15):
    owntime = datetime.datetime.now()
    expire_day = datetime.timedelta(expire)
    deadline = owntime + expire_day
    new_message = Message(content=content,
                          own=curuser,
                          deadline=deadline)
    new_message.save()
    return True
