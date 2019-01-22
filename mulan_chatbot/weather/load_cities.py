# -*- coding: utf-8 -*-

import json


def load_city():
    with open("city.json", "r") as fw:
        data = fw.read()

    city_list = []
    json_data = json.loads(data)
    for each in json_data:
        city_list.append(each["cityZh"])

    return city_list
