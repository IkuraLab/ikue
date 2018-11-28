import requests
import json
import time
import sys,os
sys.path.append(os.pardir)
import data_ikue

def req(name,iftkey):
    IFTTT_URL = 'https://maker.ifttt.com/trigger/' + name + '/with/key/' + iftkey
    data = {'value1':'0', 'value2':'0', 'value3':'0'}
    requests.post(IFTTT_URL, json = data)
    print(IFTTT_URL)

state = 0

while 1:
    city_name = "Kawasaki" 
    api = "http://api.openweathermap.org/data/2.5/weather?units=metric&q={city}&APPID={owmkey}"
    
    url = api.format(city = city_name, owmkey = data_ikue.owmkey())
    response = requests.get(url)
    data = json.loads(response.text)
    print(data['weather'][0]['main'])
    temp = data['main']['temp']
    print(temp)

    if temp > 10:
        if state == 0:
            print("扇風機を回します")
            req("switchbot1",data_ikue.iftkey())
            print("扇風機を回しました")
            state = 1
        else:
            print("既に回っているので処理をスキップします")
    elif temp < 0:
        if state == 1:
            print("扇風機を止めます")
            req("switchbot2",data_ikue.iftkey())
            print("扇風機を止めました")
            state = 0
        else:
            print("既に止まっているので処理をスキップします")
    print("10秒タンマ")
    time.sleep(10)