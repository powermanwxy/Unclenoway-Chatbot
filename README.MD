# UncleNoWay-Chatbot
这个软件是用来在匿名聊天室 [UncleNoWay (叔叔不约)](http://www.unclenoway.com)上自动聊天，并且内置了由ChatterBot驱动的AI聊天引擎。[Example](https://raw.githubusercontent.com/powermanwxy/Unclenoway-Chatbot/master/docs/example.log)
![chat_log](https://github.com/powermanwxy/Unclenoway-Chatbot/raw/master/docs/chat_log.jpg)

## 如何使用

1. 将依赖项安装文件设置为可执行，键入 `chmod +x install_dependencies.sh` ，并执行 `./install_dependencies.sh` 来安装所有的依赖项。 
>关于依赖项安装工具的更多信息, 可通过 `./install_dependencies.sh -h`来查看。
	
2. 运行 `./start.sh`. 
>如果您想让本程序以多进程运行，需要先启动IPProxyPool（代理IP池），只需以代理模式启动 `./start.sh -p`，并且修改`config.py`里的`proxy_enabled`为True。

3. *(可选)* 如果您不想使用内置的AI机器人，可以在[Tu Ling (图灵)](http://www.tuling123.com)上注册账户, 并修改 config.py文件里的 `chatbot_api_key` 与您在Tu Ling(图灵)上的密钥一致。这样的效果可能会更好，也可能不会。

4. *(可选)* 如果您不想手工的通过审查浏览器的Websocket流量来获取`usrId`，您可以在自动打码平台[Validate Platform](http://www.25531.com)上注册，并填写config.py里的`validate_api_key`。（手工获取usr_id的方式为下图，如果出现RobotTest需要重新获取）

	![get_user_id](https://github.com/powermanwxy/Unclenoway-Chatbot/raw/master/docs/get_usr_id.jpg)

顺便，您可以将您自己的语料数据以YAML格式放在`/src/training_data/`。 用上你的想象力！


## 许可证
 这个软件采用了 **GPLv3** 许可证, 只能用作学习用途。
