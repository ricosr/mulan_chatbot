# -*- coding:utf-8 -*-
import urllib.request
import re
import logging
import pickle
import traceback
from random import choice
import copy


from gevent.pywsgi import WSGIServer
from gevent import monkey
monkey.patch_all()
import falcon
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy import parse_message
from wechatpy.replies import TextReply, ImageReply
import tensorflow as tf

from poemChat import poemChat
from ElizaChat import ElizaChat
from reterival_client import Client, load_clients, select_client
from translate_l import translate
from weather.load_cities import load_city
from weather import wea
import config
from multi_turn_manage import slots, state_tracker


logging.basicConfig(filename='logger.log', level=logging.INFO)
logging.debug('debug message')


class Connect:
    def __init__(self):
        self.cache_dict = {}
        self.user_state_dict = {}
        self.user_slot_dict = {}
        self.user_domain_tracker = {}
        self.cities_list = load_city()
        load_clients()

    def judge_language(self, message):
        tmp_msg = ''
        for each_char in message:
            if each_char in config.punctuation_ls or each_char == ' ' or each_char == '\t' or each_char == '\n':
                continue
            else:
                if not 'A' < each_char < 'z':
                    return 'zh'
        return 'en'

    def on_get(self, req, resp):
        # print("get_req:{}".format(req))
        query_string = req.query_string
        query_list = query_string.split('&')
        b = {}
        for i in query_list:
            b[i.split('=')[0]] = i.split('=')[1]

        try:
            check_signature(token=config.Token, signature=b['signature'], timestamp=b['timestamp'], nonce=b['nonce'])
            resp.body = (b['echostr'])
        except InvalidSignatureException:
            pass
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        xml = req.stream.read()
        msg = parse_message(xml)
        from_user_name = self.extract_from_username(msg)
        input_language_zh = True
        if len(self.cache_dict) > 200:
            del(self.cache_dict)
            self.cache_dict = {}
        if msg.type == 'text':
            inputTxt = msg.content
            if inputTxt in self.cache_dict:
                if self.cache_dict[inputTxt]:
                    replyTxt = self.cache_dict[inputTxt]
                    reply = TextReply(content=replyTxt, message=msg)
                    del(self.cache_dict)
                    self.cache_dict = {}
                    xml = reply.render()
                    resp.body = (xml)
                    resp.status = falcon.HTTP_200
                    return
            language = self.judge_language(inputTxt)
            if language == 'en':
                input_language_zh = False
                inputTxt = translate(inputTxt, 'en')
            replyTxt, reply_type = self.getReply(inputTxt, input_language_zh, msg.id, from_user_name)
            if "@@##$$@@" not in replyTxt and replyTxt and reply_type == "chat":
                self.cache_dict[inputTxt] = replyTxt
            reply = TextReply(content=replyTxt, message=msg)
            xml = reply.render()
            resp.body = (xml)
            resp.status = falcon.HTTP_200
        elif msg.type == 'image':
            reply = ImageReply(media_id=msg.media_id, message=msg)
            xml = reply.render()
            resp.body = (xml)
            resp.status = falcon.HTTP_200

    def extract_from_username(self, msg):
        msg_para_ls = str(msg).split("), (")
        from_user_name_index = 1
        for index in range(len(msg_para_ls)):
            if "FromUserName" in msg_para_ls[index]:
                from_user_name_index = index
                break
        from_user_name = msg_para_ls[from_user_name_index].split(',')[1].strip('\'')
        return from_user_name

    # def check_city_and_weather(self, sentence):
    #     seg_list = jieba.lcut(sentence, cut_all=False)
    #     for _i, seg in enumerate(seg_list):
    #         if (seg in self.cities_ls  or seg == "天气") and seg != "木兰":
    #             return True
    #     return False

    def check_city(self, msg):
        for city in self.cities_list:
            if city in msg:
                return city
        return False

    def check_date(self, msg):
        for day_key, day_val in config.date_term_dict.items():
            if day_key in msg:
                return day_val
        return False

    def getReply(self, text, input_language_zh, msg_id, from_user_name):
        if from_user_name not in self.user_domain_tracker:
            self.user_domain_tracker[from_user_name] = ''
        default_reply = ["什么什么什么？没听懂", "我没理解你的意思，可以具体一点吗？", "主人，你在讲啥子嘛？", "我太笨，你能换个说法吗？"]
        city_name = ''
        k = 0
        try:
            replyTxt = ''
            wea_judge = False
            c = len(text)
            if c != 1:
                # TODO: NLU and intent for weather
                for wea_key_word in config.weather_key_words:
                    if wea_key_word in text:
                        wea_judge = True
                        self.user_domain_tracker[from_user_name] = "weather"
                        # self.user_dict[from_user_name] = {"weather": state_tracker.State(None)}
                        if from_user_name in self.user_state_dict:
                            if "weather" not in self.user_state_dict[from_user_name]:
                                self.user_state_dict[from_user_name] = {"weather": state_tracker.State(None)}
                                self.user_slot_dict[from_user_name] = {"weather_slot": copy.deepcopy(slots.weather_slot)}
                                self.user_state_dict[from_user_name]["weather"].add_one_state("city", None, 0)
                                self.user_state_dict[from_user_name]["weather"].add_one_state("date", None, 0)
                            else:
                                pass
                        else:
                            self.user_state_dict[from_user_name] = {"weather": state_tracker.State(None)}
                            self.user_slot_dict[from_user_name] = {"weather_slot": copy.deepcopy(slots.weather_slot)}
                            self.user_state_dict[from_user_name]["weather"].add_one_state("city", None, 0)
                            self.user_state_dict[from_user_name]["weather"].add_one_state("date", None, 0)
                        break
                if from_user_name in self.user_state_dict:  # TODO: intent for weather
                    if "weather" in self.user_state_dict[from_user_name]:
                        city = self.check_city(text)
                        if city:
                            wea_judge = True
                            self.user_domain_tracker[from_user_name] = "weather"
                            self.user_state_dict[from_user_name]["weather"].add_one_state("city", city, 1)
                            self.user_state_dict[from_user_name]["weather"].get_current_slot(self.user_slot_dict[from_user_name]["weather_slot"])
                        day = self.check_date(text)
                        if day is not None and day is not False:
                            self.user_state_dict[from_user_name]["weather"].add_one_state("date", day, 1)
                            self.user_state_dict[from_user_name]["weather"].get_current_slot(self.user_slot_dict[from_user_name]["weather_slot"])
                            wea_judge = True
                            self.user_domain_tracker[from_user_name] = "weather"
                # for city in self.cities_list:
                #     if city in text:
                #         wea_judge = True
                #         break
                # if wea_judge:
                #     for city in self.cities_list:
                #         if city in text:
                #             self.user_state_dict[from_user_name]["weather"].add_one_state("city", city, 1)
                #             self.user_state_dict[from_user_name]["weather"].get_current_slot(self.user_slot_dict[from_user_name]["weather_slot"])
                #             break
                # if wea_judge:
                #     day = 0
                #     for day_key, day_val in config.date_term_dict.items():
                #         if day_key in text:
                #             day = day_val
                #             self.user_state_dict[from_user_name]["weather"].add_one_state("date", day, 1)
                #             self.user_state_dict[from_user_name]["weather"].get_current_slot(self.user_slot_dict[from_user_name]["weather_slot"])
                #             break
                if wea_judge and from_user_name in self.user_state_dict:  # TODO: NLG dor weather
                    if "weather" in self.user_state_dict[from_user_name]:
                        reply_type = "weather"
                        self.user_state_dict[from_user_name]["weather"].get_current_slot(self.user_slot_dict[from_user_name]["weather_slot"])
                        judge_state, dialogue_state = self.user_state_dict[from_user_name]["weather"].judge_dialogue_state()
                        if not judge_state:
                            if dialogue_state == "city":
                                replyTxt = "您想查的是哪个城市呢？"
                            if dialogue_state == "date":
                                replyTxt = "今天？明天？后天？"
                            return replyTxt, reply_type
                if wea_judge:   # TODO: NLG for weather
                    judge_state, dialogue_state = self.user_state_dict[from_user_name]["weather"].judge_dialogue_state()
                    if judge_state:
                        city_name = self.user_slot_dict[from_user_name]["weather_slot"]["city"]
                        day = self.user_slot_dict[from_user_name]["weather_slot"]["date"]
                        replyTxt = wea.handle(city_name, day)
                        reply_type = "weather"
                        # del(self.user_state_dict[from_user_name])
                        return replyTxt, reply_type


            # 判断如果是一个字的话
            if c == 1 and '啊' not in text and '哼' not in text and '嗨' not in text and '好' not in text:
                print(1, self.user_domain_tracker[from_user_name])
                if self.user_domain_tracker[from_user_name] != "weather":
                    if from_user_name in self.user_state_dict:
                        self.user_state_dict.pop(from_user_name)
                        self.user_slot_dict.pop(from_user_name)
                self.user_domain_tracker[from_user_name] = "poem"
                pchat = poemChat()
                a = pchat.is_chinese(text)
                if a is False:
                    return '一个汉字呦'
                poem_flag = 24
                poem = pchat.gen_poem(text, poem_flag)
                replyTxt = pchat.pretty_print_poem(poem_=poem)
                tf.reset_default_graph()
                reply_type = "poem"

            # elif c != 1 and wea_judge is True and city_name != '':
            #     k = 3
            #     replyTxt = wea.handle(text, city_name)
            #     reply_type = "weather"

            #多于一个字走chat路线
            else:
                print(2, self.user_domain_tracker[from_user_name])
                if self.user_domain_tracker[from_user_name] != "weather":
                    if from_user_name in self.user_state_dict:
                        self.user_state_dict.pop(from_user_name)
                        self.user_slot_dict.pop(from_user_name)
                self.user_domain_tracker[from_user_name] = "chitchat"
                reply_type = "chat"
                eliza = ElizaChat()
                replyTxt = eliza.analyze(text)
                replyTxt = replyTxt
                if replyTxt == "@$@":
                    cli, cli_no = select_client()
                    replyTxt, score = cli.get_response(text, cli_no, msg_id)
            if "小通" in replyTxt:
                replyTxt = replyTxt.replace("小通", config.chatbot_name)
            if "SimSimi" in replyTxt:
                replyTxt = replyTxt.replace("SimSimi", config.chatbot_name)
            if "simsimi" in replyTxt:
                replyTxt = replyTxt.replace("simsimi", config.chatbot_name)
            if "小i" in replyTxt:
                replyTxt = replyTxt.replace("小i", config.chatbot_name)
            if "菲菲" in replyTxt:
                replyTxt = replyTxt.replace("小i", config.chatbot_name)
            if "囧囧" in replyTxt:
                replyTxt = replyTxt.replace("囧囧", config.chatbot_name)
            if input_language_zh is False and self.judge_language(replyTxt) == "zh":
                replyTxt = translate(replyTxt, 'zh')
            if replyTxt:
                return replyTxt, reply_type
            else:
                logging.info(replyTxt + reply_type + "none")
                return choice(default_reply), "none"
        except Exception as e:
            logging.error(traceback.format_exc())
            logging.error(repr(e))
            logging.error(replyTxt)
            return choice(default_reply), "err"

    # def judge_dialogue_state(self, from_user_name):
    #     if self.user_state_dict[from_user_name]:
    #         if self.user_state_dict[from_user_name]["weather"]:
    #             passprint


if __name__ == '__main__':
    app = falcon.API()
    app.add_route('/', Connect())
    server = WSGIServer(('0.0.0.0', 80), app)
    server.serve_forever()
