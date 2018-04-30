"""
This function is working with http://www.25531.com, for study propose only! If you're using this automatic validate
platform, making sure register and change the validate_api_key of <Uncle.py>. Or you can just manually capture a
usrId by inspect websocket's frames, and you have to renew this id if server emit a robot test. Author has no relevant
with this platform, so feel free to modify the code if you want to use other platform.
"""

import json
import requests
import random


def generate_usr_id(length = 17):
    alphabet = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890"
    usr_id = ""

    for i in range(length):
        n = random.random()
        n = round(62 * n)
        usr_id += alphabet[int(n - 1)]

    return usr_id


def get_user_id(logger, validate_api_key, website_t_num):
    api_count_url = 'http://jiyan.25531.com/api/info'

    check_params = {'appkey': validate_api_key}
    available_request = requests.get(api_count_url, params=check_params)
    available_list = json.loads(available_request.text)

    if available_list['data']['flag'] is True:
        available_count = available_list['data']['msg']
        available_str = 'Validate SDK available remain:' + str(available_count)
        print available_str
        logger.info(available_str)
    else:
        print 'error:', available_list['code']
        logger.error(available_list['code'])

    validate_url = 'http://47.104.124.125:3001/geetest/register?t=' + website_t_num
    uncle_validate_info = requests.get(validate_url)
    uncle_validate_info = json.loads(uncle_validate_info.text)

    challenge = uncle_validate_info['challenge']
    gt = uncle_validate_info['gt']
    success = uncle_validate_info['success']

    validate_api_url = 'http://jiyan.25531.com/api/create'
    referer = 'http://www.unclenoway.com/'
    model = success

    validate_params = {'gt': gt, 'challenge': challenge, 'referer': referer, 'appkey': validate_api_key, 'model': model}
    r = requests.get(validate_api_url, params=validate_params)
    r = json.loads(r.text)

    code = r['code']
    if code == 10000:
        respond_challenge = r['data']['challenge']
        respond_validate = r['data']['validate']

    else:
        print 'Detect error!'
        logger.error('Validate Filed!')
        return ''

    post_url = 'http://47.104.124.125:3001/geetest/validate'
    usr_id = generate_usr_id()

    sec_code = respond_validate + '|jordan'
    post_data = {'geetest_challenge': respond_challenge, 'geetest_validate': respond_validate,
                 'geetest_seccode': sec_code, 'ip': '{"ip":""}', 'userId': usr_id}

    ans = requests.post(post_url, data=post_data)
    ans = json.loads(ans.text)

    if ans['status'] == 'success':
        uncle_status_str = 'Get new usrId: ' + usr_id
        print uncle_status_str
        logger.info(uncle_status_str)
    else:
        print 'error', ans
        logger.error(ans)

    return usr_id
