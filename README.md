# 木兰聊天机器人

## 部署步骤:
 * 目录model为存放RNN模型目录, 需要从其目录README.md指定链接下载模型文件到model目录中
 * 安装依赖包: `pip3 install -r requirements.txt`
 
## 启动步骤:
* 启动命令: `nohup python3 connect.py &`
* **注意: 该方法服务会监听在10010端口**
* 说明: 每当有IR请求, connect.py会实例化一个reterival_client.Client类对象, 连接本地10086端口的IR的服务
* 在启动后，再在微信公众号管理平台上填写服务器地址(URL)和令牌(Token), Token在config.py中文件配置

## 环境要求:
* Python3
* 最好是Linux, Windows上微信依赖库安装会出现问题

## 其他说明:
* 需要配合https://github.com/ricosr/retrieval_chatbot 一起使用

# mulan_chatbot

## deploy steps:
* folder model is to save RNN model, you need to download the model files into folder model according to the URL of README.md in model folder
* install requirement packages: `pip3 install -r requirements.txt`

## start steps:
* starting command: `nohup python3 connect.py &`
* **attention: this way will listen port 10010**
* explanation: when there is a IR request, connect.py will build a object of reterival_client.Client, which can connect local IR server through 10086 port
* after starting, you need to set the server URL and Token in management platform of WeChat Official Account, you can change Token in config.py

## environment requirement:
* Python3
* Operating system had better be Linux, if Windows you need to install VS2010+

## other introduction:
* this project need to be deployed with https://github.com/ricosr/retrieval_chatbot together