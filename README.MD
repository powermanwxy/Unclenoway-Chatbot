# UncleNoWay-Chatbot
	This page currently is under construction.
This software is an automatic chatting tool for anonymous chat room [UncleNoWay (叔叔不约)](http://www.unclenoway.com).

## How to use

1. Install these packages that all available in pip.

	- requests
	- websocket
	- termcolor
	
2. If you want to run this in muti-processes, then install the [IPProxyPool](https://github.com/qiyeboy/IPProxyPool) , and making sure the server is running at `127.0.0.1:1024`. Modify the Uncle.py `proxy_enabled = True` If you're using another port, replace the Uncle.py `proxy_url` identical with your setting.

3. Register at [Tu Ling (图灵)](http://www.tuling123.com), and modify Uncle.py `chatbot_api_key` identical with the key from Tu Ling. You can replce this function in order to use your own chatbot platform.

3. *(Optional)* Register at [Validate Platform](http://www.25531.com), and modify Uncle.py `validate_api_key`. If you don't want to use the automatic validate platform, you can also manualy get your `usrId` by inspect your network's websocket connection.

## Licence
 This software is following **GPLv3**, for study propose only!