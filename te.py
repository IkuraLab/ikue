import pyaudio
import wave
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

def music(name,buffer):
    input_filename = name
    buffer_size = buffer
    wav_file = wave.open(input_filename , 'rb')
    p = pyaudio.PyAudio()
    stream = p.open (
                     format = p.get_format_from_width ( wav_file . getsampwidth ()) ,
                     channels = wav_file.getnchannels () ,
                     rate = wav_file.getframerate () ,
                     output = True
                     )
    remain = wav_file.getnframes ()
    while remain > 0:
        buf = wav_file.readframes ( min ( buffer_size , remain ))
        stream.write ( buf )
        remain -= buffer_size
    stream.close ()
    p.terminate ()
    wav_file.close ()

state = 0
temp_pref = 10

while 1:
    city_name = "Kawasaki" 
    api = "http://api.openweathermap.org/data/2.5/weather?units=metric&q={city}&APPID={owmkey}"
    
    url = api.format(city = city_name, owmkey = data_ikue.owmkey())
    response = requests.get(url)
    data = json.loads(response.text)
    print(data['weather'][0]['main'])
    temp = data['main']['temp']
    print(temp)

    if temp >= temp_pref:
        if state == 0:
            print("扇風機を回します")
            req("switchbot1",data_ikue.iftkey())
            print("扇風機を回しました")
            state = 1
            music('music/syamu.wav',4096)
        else:
            print("既に回っているので処理をスキップします")
    elif temp < temp_pref:
        if state == 1:
            print("扇風機を止めます")
            req("switchbot2",data_ikue.iftkey())
            print("扇風機を止めました")
            state = 0
            music('music/jinja.wav',4096)
        else:
            print("既に止まっているので処理をスキップします")
    print("10秒タンマ")
    time.sleep(10)