import os
import time
import requests
from datetime import datetime
from subprocess import call

import city_dict

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'

def ciba_words():
	resp = requests.get('http://open.iciba.com/dsapi')
	if resp.status_code == 200:
	    content_dict = resp.json()
	    content = content_dict.get('content')
	    note = content_dict.get('note')
	    return '\n{}\n{}\n'.format(content, note)
	else:
		return ""    

def weather_tips(city_code):
	weather_url = 'http://t.weather.sojson.com/api/weather/city/{}'.format(city_code)
	
	resp = requests.get(url=weather_url)

	if resp.status_code == 200 and resp.json().get('status') == 200:
		weather_dict = resp.json()
		
		# 今日天气
		today_weather = weather_dict.get('data').get('forecast')[1]
		
		# 今日日期
		today_time = (datetime.now().strftime('今日天气(%Y{y}%m{m}%d{d})\n').format(y='年', m='月', d='日'))

		# 今日天气注意事项
		notice = today_weather.get('notice')
		# 温度
		high = today_weather.get('high')
		high_c = high[high.find(' ') + 1:]
		low = today_weather.get('low')
		low_c = low[low.find(' ') + 1:]
		temperature = '温度 : {}/{}'.format(low_c, high_c)

		# 风
		wind_direction = today_weather.get('fx')
		wind_level = today_weather.get('fl')
		wind = '{} : {}'.format(wind_direction, wind_level)

		# 空气指数
		aqi = today_weather.get('aqi')
		aqi = '空气指数 : {}'.format(aqi)

		dictum_msg = '每日格言:' + ciba_words()

		today_msg = (
		    '{today_time}\n{notice}。\n{temperature}\n'
		    '{wind}\n{aqi}\n\n{dictum_msg}'.format(
		        today_time=today_time, notice=notice,
		        temperature=temperature, wind=wind, aqi=aqi, dictum_msg=dictum_msg))

		return today_msg
	else:
		return ""

def notify(message):
	message = 'display notification "{}" with title "每日天气"'.format(message)
	call(["osascript", "-e", message])

city_code = city_dict.city_dict.get("北京")

msg = weather_tips(city_code)

print(msg)

notify(msg)


