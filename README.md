# mulan_chatbot

## 部署:
 * 目录model为存放RNN模型目录, 需要从其目录README.md指定链接下载模型文件到model目录中
 * 安装依赖包`pip3 install -r requirements.txt`
 
## 启动方法:
* 启动命令: `nohup python3 connect.py &`
* **注意: 该方法服务会监听在10010端口**
* 说明: 每当有IR请求, connect.py会实例化一个reterival_client.Client类对象, 连接本地10086端口的IR的服务
* 在启动后，再在微信公众号管理平台上填写服务器地址(URL)和令牌(Token), Token在config.py中文件配置

## 运行环境:
* Python3
* 最好是Linux, Windows上微信依赖库安装会出现问题

## 其他:
* 需要配合https://github.com/ricosr/retrieval_chatbot 一起使用