# -*- coding: utf-8 -*-

import requests


def weather(city_name, day):
    # try:
        weather_info = requests.get('https://www.tianqiapi.com/api/?version=v1&city={}&appid=12345678&appsecret=abcdwfg'.format(city_name))
        weather_info.encoding = weather_info.apparent_encoding
        # print(weather_info.json())
        weather_dict = extract_info(weather_info.json())
        return weather_dict[day]
    # except Exception as e:
    #     return 0


def extract_info(json_info):
    # print(json_info)
    weather_dict = {}
    exp_judge = False
    two_win = False
    update_time = "更新时间:" + json_info["update_time"]
    city = json_info["city"]
    head_info = city + '\n'
    data = json_info["data"]
    for i in range(len(data)):
        date = data[i]["date"]
        week = data[i]["week"]
        wea = data[i]["wea"]
        try:
            air = data[i]["air"]
            air_level = data[i]["air_level"]
            air_tips = data[i]["air_tips"]
            alarm = data[i]["alarm"]
        except:
            exp_judge = True
            pass
        tem1 = data[i]["tem1"]
        tem2 = data[i]["tem2"]
        tem = data[i]["tem"]
        win1 = data[i]["win"][0]
        if len(data[i]["win"]) > 1:
            two_win = True
            win2 = data[i]["win"][1]
        win_speed = data[i]["win_speed"]

        friendly_reference = data[i]["index"]
        ref_info = ''
        for ref in friendly_reference:
            if ref["title"]:
                if "em>" in ref["title"]:
                    ref_info += "运动健康" + ':'
                else:
                    ref_info += ref["title"] + ':'
            if ref["level"]:
                ref_info += ref["level"] + ','
            if ref["desc"]:
                ref_info += ref["desc"] + '\n'
        if i == 0:
            body_info = date + ',' + week + '\n' + wea + '\n' + "最高:{}".format(tem1) + "~~" + "最低:{}".format(tem2) + ",当前温度:{}".format(tem) + '\n'
        else:
            body_info = date + ',' + week + '\n' + wea + '\n' + "最高:{}".format(tem1) + "~~" + "最低:{}".format(tem2) + '\n'
        if exp_judge is False:
            if air:
                body_info = body_info + "空气指数:{}({}), {}".format(air, air_level, air_tips) + '\n'
            if alarm:
                body_info += "!!预警!!:{}{}预警, {}".format(alarm["alarm_type"], alarm["alarm_level"], alarm["alarm_content"]) + '\n'
        if two_win:
            body_info = body_info + "{}转{}, {}".format(win1, win2, win_speed) + '\n'
        else:
            body_info = body_info + "{}, {}".format(win1, win_speed) + '\n'
        body_info = body_info + ref_info
        weather_dict[i] = head_info + body_info + '\n' + update_time
    return weather_dict


def handle(city_name, day):
    # city_name = "香港"
    # day = 0
    # day_key_word = {"今": 0, "明": 1, "后": 2}
    # # for city in cities_list:
    # #     if city in message:
    # #         city_name = city
    # for day_key, day_val in day_key_word.items():
    #     if day_key in message:
    #         day = day_val
    reply = weather(city_name, day)
    return reply if reply else '不会自己去看天气预报啊'


# if __name__ == '__main__':
#     # import load_cities
#     print(handle("今天北京天气", "北京"))
