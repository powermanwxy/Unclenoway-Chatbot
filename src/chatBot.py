#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""
This function is working with http://www.tuling123.com. Making sure register and change the chatbot_api_key
of <Uncle.py>.
"""

import json
import requests

url = 'http://openapi.tuling123.com/openapi/api/v2'
# Cause we haven't support sending image yet, if chatbot send a image back, we just send the default respond.
respond = '...'


def get_message_from_bot(logger, usr_id, usr_city, partner_msg, chatbot_api_key):

    global respond

    data = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": unicode(partner_msg)
            },
            "selfInfo": {
                "location": {
                    "city": unicode(usr_city),
                    "province": "",
                    "street": ""
                }
            }
        },
        "userInfo": {
            "apiKey": chatbot_api_key,
            "userId": usr_id
        }
    }

    data = json.dumps(data, ensure_ascii=False).encode('utf-8')

    try:
        r = requests.post(url, data=data)
        ans = json.loads(r.text)

        err_code = ans['intent']

        if err_code['code'] == 4003:
            print ('ChatBot SDK over usage')
            logger.error('ChatBot SDK over usage')
            return respond

        elif int(err_code['code']) < 10000:
            error_str = 'ChatBot SDK Error Code: ' + str(err_code['code'])
            print (error_str)
            logger.error(error_str)

            return respond

        ans = ans['results'][0]
        # print ans

        if ans['resultType'] == 'text':
            respond = ans['values']['text']
            respond = json.dumps(respond, ensure_ascii=False)
            respond = respond[1:len(respond)-1]
            return respond
        else:
            return respond

    except Exception as e:
        print e
        logger.error(e)
