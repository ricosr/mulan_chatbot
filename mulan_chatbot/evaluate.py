from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
deepThought = ChatBot("deepThought")
deepThought.set_trainer(ChatterBotCorpusTrainer)
# 使用中文语料库训练它
deepThought.train("chatterbot.corpus.chinese")  # 语料库

while True:
    question=input("请输入你的对话: ")
    print(deepThought.get_response(question))