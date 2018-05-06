# UncleNoWay-Chatbot
This software is an automatic chatting robot for anonymous chat room [UncleNoWay (叔叔不约)](http://www.unclenoway.com).
![chat_log](https://github.com/powermanwxy/Unclenoway-Chatbot/raw/master/docs/chat_log.jpg)

## How to use

1. Set the installation script excuatable by `chmod +x install_dependencies.sh` and run `./install_dependencies.sh` to install the dependencies. 
>For more infomation about installation tool, please type `./install_dependencies.sh -h`
	
2. Run `./start.sh`. 
>If you want to run this in muti-processes, then starting the IPProxyPool with `./install_dependencies.sh -p`

3. *(Optional)* If you don't want to use the built-in chatbot, you can register at [Tu Ling (图灵)](http://www.tuling123.com), and modify config.py `chatbot_api_key` identical with the key from Tu Ling. This might bring you a better result, or not.

4. *(Optional)* If you don't want to manualy get your `usrId` by inspect your network's websocket connection, then you can register at [Validate Platform](http://www.25531.com), and fill in config.py `validate_api_key`. 

	![get_user_id](https://github.com/powermanwxy/Unclenoway-Chatbot/raw/master/docs/get_usr_id.jpg)

By the way, you can add your own conversition data in order to train the chatbot, just add them to `/src/training_data/` with yaml format. Just using your imagination. 


## Licence
 This software is following **GPLv3**, for study propose only!
