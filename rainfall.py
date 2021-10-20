#!/usr/bin/python3

#rainfall 
def rainfall(lon,lat,crient_id):
    import urllib.request
    import json,time
    #rainfall
    base_url = 'https://map.yahooapis.jp/weather/V1/place?'
    

    # yahoo APIを使うためのKEY(事前登録が必用)
    url = '%scoordinates=%s,%s&appid=%s&output=json' % (base_url, str(lon),str(lat), crient_id)
    response = urllib.request.urlopen(url).read()
    data_json = json.loads(response.decode('utf-8'))
    weather_info = data_json['Feature'][0]['Property']['WeatherList']['Weather']
    base_minutes = 10
    for i in range(6):
        print(" ")
# enumerateメソッドでindexを取得しながらループをまわす
    for index, var in enumerate(weather_info):
# 降水強度より、メッセージをretrun_rain_level関数から取得
            info = retrun_rain_level(var['Rainfall'])
            if index == 0:
                before_words = " 今、"
                if var['Rainfall'] == 0.0:
                    after_words = "っていない"
                else:
                    after_words = "っている"
            else:
                before_words = ' %s分後、' % (base_minutes)
                if var['Rainfall'] == 0.0:
                    after_words = "らないだろう"
                else:
                    after_words = "るだろう"
                base_minutes += 10
            print(before_words + info )
            print("\033[34m   %s mm/h \033[0m" %str(var['Rainfall'])) 
            #print(var['Rainfall'] )
            time.sleep(2)
def retrun_rain_level(rainfall):
        if (rainfall == 0.0):
            rain_level = "雨は降らない"
        elif (rainfall < 1.0):
            rain_level = "雨、ぽつぽつ"
        elif (rainfall < 2.0):
            rain_level = "弱い雨、しとしと"
        elif (rainfall < 3.0):
            rain_level = "やや強い雨、サー"
        elif (rainfall < 20.0):
            rain_level = "やや強い雨、ザーザー"
        elif (rainfall < 30.0):
            rain_level = "土砂降り"
        elif (rainfall < 40.0):
            rain_level = "バケツをひっくり返したよう"
        elif (rainfall < 50.0):
            rain_level = "滝のように非常に激しい雨"
        elif (rainfall >= 50.0):
            rain_level = "猛烈な雨が降る"
        return rain_level                

if __name__ == "__main__":

    lon = 135
    lat = 35
    rainfall(lon,lat)