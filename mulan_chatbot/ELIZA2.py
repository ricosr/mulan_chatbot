import random
import re
import urllib.request
reflections = {
    "我": "你",
    "我会": "你会",
    "我有": "你有",
    "我将": "你将",
    "我们": "你们",
    "你": "我",
    "你有": "我有",
    "你将": "我将",
    "你们": "我们",
    "你的": "我的",

}

psychobabble = [
    [r'我需要 (.*)',
     ["为什么你需要 {0}?",
      "它真的会帮助你获得 {0}?",
      "你确定你需要 {0}?"]],

    [r'quit',
     ["谢谢你跟我说话.",
      "再见.",
      "谢谢，祝你有美好的一天!"]],

    [r'(.*)',
     ["我不太明白你的意思"]]
]


def reflect(fragment):
    tokens = fragment.lower().split()
    for i, token in enumerate(tokens):
        if token in reflections:
            tokens[i] = reflections[token]
    return ' '.join(tokens)


def analyze(statement):
    for pattern, responses in psychobabble:
        match = re.match(pattern, statement.rstrip(".!"))
        if match:
            response = random.choice(responses)
            return response.format(*[reflect(g) for g in match.groups()])


def main():
    print("你好。你今天感觉如何？")

    while True:
        statement = input("YOU: ")
        replyTxt=analyze(statement)
        if replyTxt == "我不太明白你的意思":
            x = urllib.parse.quote(statement)
            link = urllib.request.urlopen(
                "http://nlp.xiaoi.com/robot/webrobot?&callback=__webrobot_processMsg&data=%7B%22sessionId%22%3A%22ff725c236e5245a3ac825b2dd88a7501%22%2C%22robotId%22%3A%22webbot%22%2C%22userId%22%3A%227cd29df3450745fbbdcf1a462e6c58e6%22%2C%22body%22%3A%7B%22content%22%3A%22" + x + "%22%7D%2C%22type%22%3A%22txt%22%7D")
            html_doc = link.read().decode()
            reply_list = re.findall(r'\"content\":\"(.+?)\\r\\n\"', html_doc)
            print("小i：" + reply_list[-1])
            replyTxt = reply_list[-1]
        else:
            print("ELIZA: " + analyze(statement))

        if statement == "quit":
            break


if __name__ == "__main__":
    main()
