# -*- coding: UTF-8 -*-

# Chat timeout
chat_timeout = 120
# Log filename format: date-uncleInstanceIndex-partnerIndex.log
log_path = "Logs/"

# Proxy might be unstable, if you're not running this in multiprocessing, suggest just don't use proxy.
proxy_enabled = False
# This has to match with IPProxyPool's config.
proxy_url = 'http://127.0.0.1:8000'

# Chatbot's type: 1 = built in, 2 = Tu Ling
# If you're using Tu Ling, don't forgot to define chatbot_api_key
chatbot_type = 1
# Chatbot's gender: f/m
chatbot_gender = 'f'
# Chatbot's city, currently only support cities in China.
chatbot_location = u'北京'
# Chatbot's age: [1:3], 1 = 18-, 2 = 19 ~ 23, 3 = 23+
chatbot_age = 2
# Cause the chatbot haven't support image yet, this is the default responding if partner sends a image.
chatbot_img_respond = u'哇厉害了hhh'

# See <validate.py>. If this is not empty, automatic validate platform will NOT be used.
# You have to define either usr_id or validate_api_key
usr_id = ''
# Validate platform api key. http://www.25531.com
validate_api_key = ''
# Chatbot platform api key. http://www.tuling123.com
chatbot_api_key = ''

# Magic word, you might change this if the program is not working, otherwise just keep it default.
website_t_num = '1525060720598'
website_t_str = 'MDKizZH'
