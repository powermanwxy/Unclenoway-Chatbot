# -*- coding: UTF-8 -*-
import requests
import json
import websocket
import logging
import random
import time
import threading
from termcolor import *
import os

import chatBot
import validate
import proxy

# Chat timeout
chat_timeout = 120
# Log filename format: date-uncleInstanceIndex-partnerIndex.log
log_path = "Logs/"

# Proxy might be unstable, if you're not running this in multiprocessing, suggest just don't use proxy.
proxy_enabled = False
# This has to match with IPProxyPool's config.
proxy_url = 'http://127.0.0.1:1024'

# Chatbot's gender: f/m
chatbot_gender = 'f'
# Chatbot's city, currently only support cities in China.
chatbot_location = u'北京'
# Chatbot's age: [1:3], 1 = 18-, 2 = 19 ~ 23, 3 = 23+
chatbot_age = 2
# Cause the chatbot haven't support image yet, this is the default responding if partner sends a image.
chatbot_img_respond = u'哇厉害了hhh'

# See <validate.py>. If this is not empty, automatic validate platform will NOT be used.
usr_id = ''
# Validate platform api key. http://www.25531.com
validate_api_key = ''
# Chatbot platform api key. http://www.tuling123.com
chatbot_api_key = ''

# Magic word, you might change this if the program is not working, otherwise just keep it default.
website_t_num = '1525060720598'
website_t_str = 'MDKizZH'

# Don't change the code below unless you know what you are doing.


class PingPongSender(threading.Thread):
    # sending pingpong to keep long connection
    def __init__(self, ws, logger):
        threading.Thread.__init__(self)
        self.loop = False
        self.ws = ws
        self.logger = logger

    def run(self):
        self.loop = True
        while self.loop:
            time.sleep(30)
            try:
                self.ws.send('2')
            except:
                print 'Ping Pong Error!'
                self.logger.error('Ping-Pong Error!')
                self.ws.close()


class TimeController(threading.Thread):
    # request new partner if partner not typing or sending anything within chat_timeout seconds
    def __init__(self, ws, logger, sender):
        threading.Thread.__init__(self)
        self.loop = False
        self.time_left = chat_timeout
        self.ws = ws
        self.logger = logger
        self.new_partner_request = sender

    def run(self):
        self.loop = True
        while self.loop:
            if self.time_left == 0:
                try:
                    self.time_left = chat_timeout

                    send_str = '42["syscmd",{"msg":"end"}]'
                    self.ws.send(send_str)

                    self.new_partner_request(self.ws)

                    print(colored('Timeout, request new partner.', 'yellow'))
                    self.logger.info('Timeout, request new partner.')
                except:
                    print(colored('Timeout error.', 'yellow'))
                    self.logger.error('Timeout error.')
                    self.ws.close()
            else:
                time.sleep(1)
                self.time_left -= 1

                if self.time_left < 5:
                    print 'Timeout left: ', self.time_left


class Uncle:
    def __init__(self, index=0):
        self.first_time = True
        self.loop = True

        self.usr_id = usr_id
        self.chatbot_id = ''

        self.proxy_address = []
        self.instance_index = index
        self.partner_count = 0

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        self.pingpong_sender = None
        self.time_controller = None
        self.fh = None

        if self.usr_id == '' and validate_api_key == '':
            print 'You have to define either usr_id or validate_api_key!'
            print 'Stop!'
            self.loop = False

        if chatbot_api_key == '':
            print 'You have to define chatbot_api_key!'
            print 'Stop!'
            self.loop = False

        if self.instance_index > 4:
            self.loop = False

    def start(self):
        if not os.path.isdir('Logs/'):
            os.mkdir(log_path)

        self.create_new_log()

        servers_list_json = requests.get('http://api.unclenoway.com:3602/user-count/')
        servers = json.loads(servers_list_json.text)

        servers_list = []
        for item in servers:
            servers_list.append(item)

        socket_server = servers_list[-1]
        socket_url = socket_server['server']['socket']

        print 'Server user count: ', socket_server['data']['userCount'], ', female: ', socket_server['data']['female']

        while self.loop:
            sid_request = requests.get('http://' + socket_url + '/socket.io/?EIO=3&transport=polling&t='
                                       + website_t_str)
            sid_str = sid_request.text[4:len(sid_request.text) - 4]
            sid = json.loads(sid_str)['sid']
            print 'Sid: ', sid

            cookie = sid_request.headers['set-cookie']
            cookie = cookie[3:len(cookie) - 18]

            ws_url = 'ws://' + socket_url + '/socket.io/?EIO=3&transport=websocket&sid=' + sid
            print 'Connecting: ', ws_url

            ws = websocket.WebSocketApp(ws_url,
                                        header={
                                            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) '
                                                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                                                          'Chrome/67.0.3393.4 Safari/537.36',
                                            'Upgrade': 'websocket',
                                            'Connection': 'Upgrade'
                                        },
                                        cookie='io=' + cookie,
                                        on_close=self.on_close,
                                        on_message=self.on_message,
                                        on_error=self.on_error
                                        )
            ws.on_open = self.on_open

            self.pingpong_sender = PingPongSender(ws, self.logger)
            self.time_controller = TimeController(ws, self.logger, self.request_new_user)

            if proxy_enabled:
                self.proxy_address = proxy.get_proxy(self.logger, proxy_url, self.instance_index)
                print 'Proxy address: ', self.proxy_address[0]
                ws.run_forever(http_proxy_host=self.proxy_address[0], http_proxy_port=self.proxy_address[1])

            else:
                ws.run_forever()

            ws.close()
            time.sleep(5)

    def on_open(self, ws):

        ws.send("2probe")
        ws.send("5")

        while self.usr_id == '':
            self.usr_id = validate.get_user_id(self.logger, validate_api_key, website_t_num)

        self.request_new_user(ws)

    def on_message(self, ws, message):
        self.phrase_received_data(message, ws)

    def on_error(self, ws, error):

        self.time_controller.loop = False
        self.pingpong_sender.loop = False

        print("### Error ###")
        print(error)
        self.logger.error("### Error ###")
        self.logger.error(error)

        if str(error) != '' and proxy_enabled:
            proxy.delete_proxy(self.logger, proxy_url, self.proxy_address[0])
            print 'Delete IP: ', self.proxy_address[0]

    def on_close(self, ws):
        self.pingpong_sender.loop = False
        self.time_controller.loop = False

        print("### closed ###")
        self.logger.error("### closed ###")

    def create_new_log(self):

        name = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        logfile = log_path + name + '-' + str(self.instance_index) + '-' + str(self.partner_count) + '.log'

        self.fh = logging.FileHandler(logfile, mode='w')
        self.fh.setLevel(logging.DEBUG)

        formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
        self.fh.setFormatter(formatter)
        self.logger.addHandler(self.fh)

        instance_str = 'From instance: ' + str(self.instance_index)
        self.logger.info(instance_str)

    def phrase_received_data(self, received_str, ws):

        if received_str == '3probe':
            print 'Probe received'
            self.logger.debug('Probe received')
            self.pingpong_sender.start()
            self.time_controller.start()
            return

        elif received_str == '3':
            print 'Ping-pong received.'
            self.logger.debug('Ping-pong received.')
            return

        received_str = received_str[2:len(received_str)]
        data = json.loads(received_str)

        if data[0] == 'syscmd':
            if isinstance(data[1], basestring):
                if data[1] == 'connected':
                    print 'Init connected.'
                    self.logger.debug('Init connected.')
                else:
                    print 'Your sid:', data[1]
                    self.logger.debug('Your sid: %s', data[1])

            elif isinstance(data[1], dict):
                item = data[1]
                if item['msg'] == 'connecting':
                    print 'Init connecting.'
                    self.logger.debug('Init connecting.')

                elif item['msg'] == 'connected':
                    self.partner_count += 1

                    if self.first_time is False:
                        self.logger.removeHandler(self.fh)
                        self.create_new_log()

                        print(colored('New Log File.', 'yellow'))
                        self.logger.info('New log file created.')

                    else:
                        self.first_time = False
                        self.time_controller.time_left = chat_timeout

                    labels = item['labels']
                    if len(labels) is not 0:
                        label_str = ' Label:'
                        for l in labels:
                            label_str += " " + l['name']
                    else:
                        label_str = ''

                    partner_info = 'Connected ' + item['partnerInfoObj']['province'] + \
                                   item['partnerInfoObj']['strGender'] + \
                                   item['partnerInfoObj']['strAge'] + item['partnerInfoObj']['province'] + \
                                   item['partnerIp'][7:len(item['partnerIp'])] + label_str

                    print(colored(partner_info, 'yellow'))
                    self.logger.info(partner_info)

                    self.chatbot_id = self.get_chatbot_id()

                elif item['msg'] == 'reconnected':
                    ws.send('42["syscmd",{"msg":"end"}]')

                    self.request_new_user(ws)

                    print (colored('Reconnected, new request...', 'yellow'))
                    self.logger.debug('Reconnected, new request...')

                elif item['msg'] == 'endByPartner':

                    self.request_new_user(ws)

                    print (colored('End by partner, new request...', 'yellow'))
                    self.logger.info('End by partner, new request...')

                elif item['msg'] == 'broadcast':
                    print (colored('Not allowed to send image within 2 min from beginning.', 'yellow'))
                    self.logger.warning('Not allowed to send image within 2 min from beginning.')

                elif item['msg'] == 'ack':
                    print 'Ack'
                    self.logger.debug('Ack')

                elif item['msg'] == 'end':
                    print 'User ended chat.'
                    self.logger.debug('User ended chat.')

                elif item['msg'] == 'disconnect':
                    print(colored('Server has ended connection.', 'red'))
                    self.logger.error('Server has ended connection.')
                    ws.close()

                elif item['msg'] == 'myIp':
                    print 'IP test.'
                    self.logger.debug('IP test.')

                elif item['msg'] == 'robotTest':
                    print(colored('Robot Test.', 'yellow'))
                    self.logger.warning('Robot Test.')
                    ws.send('41')

                    self.pingpong_sender.loop = False
                    self.time_controller.loop = False
                    self.usr_id = ''

                    ws.close()

                else:
                    print(colored('Unknown', 'red'), received_str)
                    self.logger.warning(received_str)

        elif data[0] == 'msgRead':
            print 'Partner has read your message.'
            self.logger.debug('Partner has read your message.')

        elif data[0] == 'typing':
            print 'Partner is typing....'
            self.logger.debug('Partner is typing....')

            self.time_controller.time_left = chat_timeout

        elif data[0] == 'strangerMessage':
            partner_info = '###StrangerMsg: ' + data[1]['content']
            print(colored(partner_info, 'red'))
            self.logger.info(partner_info)

            self.time_controller.time_left = chat_timeout

            msg_read = ['syscmd', {"msg":"msgRead","msgId": data[1]['msgId']}]
            msg_read_str = '42' + json.dumps(msg_read, ensure_ascii=False)
            ws.send(msg_read_str)

            print "Send partner a receipt."
            self.logger.debug("Send partner a receipt.")

            if data[1]['options']['isImage'] is True:
                chat_bot_respond = chatbot_img_respond
            else:
                chat_bot_respond = chatBot.get_message_from_bot(self.logger, self.chatbot_id,
                                                                chatbot_location, data[1]['content'], chatbot_api_key)

            n = random.random()
            n = round(3 * n) + 3
            print 'Sleep: ', n
            self.logger.debug('Sleep: %d', n)

            time.sleep(n)
            msg_id = self.get_msg_id()

            for i in range(len(chat_bot_respond)):
                ws.send('42["typing",null]')
                time.sleep(0.3)
                print 'Chatbot is typing....'

            msg_send = ["clientMessage", {"msgId": msg_id, "content": chat_bot_respond,
                                          "options": {"emitPartner": False, "msgId": msg_id,
                                                      "isImage": False}}]
            msg_send_str = '42' + json.dumps(msg_send).decode('utf-8')
            ws.send(msg_send_str)

            partner_info = '###ChatBotMsg: ' + chat_bot_respond
            print (colored(partner_info, 'red'))
            self.logger.info(partner_info)

        else:
            print(colored('Unknown', 'red'), received_str)
            self.logger.warning(received_str)

    def request_new_user(self, ws):
        request = ["syscmd", {"msg": "new", "gender": chatbot_gender, "province": chatbot_location,
                              "isSelfStayStr": False, "age": chatbot_age, "savedId": self.usr_id,
                              "isShowLocation": True, "wordFilter": 1}]
        request_str = '42' + json.dumps(request, ensure_ascii=False)

        ws.send(request_str)

    def get_chatbot_id(self, length=17):
        alphabet = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890"
        chatbot_id = ""

        for i in range(length):
            n = random.random()
            n = round(62 * n)
            chatbot_id += alphabet[int(n - 1)]

        print 'UsrChatBotID: ', chatbot_id
        self.logger.info('UsrChatBotID: %s', chatbot_id)

        return chatbot_id

    def get_msg_id(self):
        now = time.time()
        n = random.random()
        msg_id = 'm' + str(int(now * 1000)) + str(int(round(n * 10)))
        # print 'msgID: ',msg_id
        return msg_id
