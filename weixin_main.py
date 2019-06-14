import itchat
import re
import requests
import json
import threading
if_weather=False
if_seven=False
future=''
city_list={'南京':'1','兰溪':'2','巢湖':'3','杭州':'4'} #天气列表
@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    global if_weather,future,if_seven
    message=msg.text
    if(if_seven):
        if('7' in message):
            msg.user.send(future)
        else:
            msg.user.send('不查询七天天气')
        if_seven=False
    if(if_weather):
        try:
            num=int(message)
            if(num>4):
                raise RuntimeError('testError')
        except BaseException:
            msg.user.send('输入有误，请重新输入或者输入取消')
        else:
            city_number={v:k for k,v in city_list.items()}
            today,future=weather(city_number[str(num)])
            msg.user.send(today)
            msg.user.send('回复 7 获取接下来7天的天气')
            if_seven=True
            if_weather=False
        if('取消' in message):
            if_weather=False
            msg.user.send('指令已取消')
    if('天气' in message):
        if_weather=True
        lists=''
        for key,value in city_list.items():
            lists+='%s:%s\n'%(key,value)
        msg.user.send('请回复下列数字')
        msg.user.send(lists)
    

def weather(cityname):
    '''
    cityname 城市名称 msg_for:发送给人
    '''
    data={'cityname':cityname.encode('utf8'),'dtype':'json','format':'2','key':'43f90a821989f0bd1a4f1c4ffa04b22c'}
    r=requests.get('http://v.juhe.cn/weather/index',params=data)
    result=json.loads(r.text).get('result')
    today_dict=result.get('today')
    future_dict=result.get('future')
    today='天气:'+today_dict['weather']+'\n'+'温度:'+today_dict['temperature']+'\n'+'风向:'+today_dict['wind']+'\n'+'穿衣指南:'+today_dict['dressing_advice']
    future=''
    for item in future_dict:
        list='日期'+item['date']+' '+item['week']+'\n'+'天气:'+item['weather']+'\n'+'温度:'+item['temperature']+'\n'+'-----------\n'
        future+=list
    return today,future
################################
def time_weather():
    



itchat.auto_login(hotReload=True)
#author=itchat.search_friends(name='小sky')[0]
#author.send('1111')
itchat.run()


#result=weather('南京')
