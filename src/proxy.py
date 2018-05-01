"""
This function is working with https://github.com/qiyeboy/IPProxyPool. If you want to connect server through proxy,
you have to run IPProxyPool first, and the config has to identical. Making sure the pool has enough proxies.
"""

import requests
import json


def get_proxy(logger, proxy_url, index):
    # Get proxy server info from pool.
    try:
        r = requests.get(proxy_url)
        data = json.loads(r.text)
    except:
        print 'Connect proxy server error!'
        logger.error('Connect proxy server error!')
        return []

    if index > len(data):
        print "Index over current proxy count."
        logger.error('Index over current proxy count.')
        return []

    # data = ["101.81.141.175", 9999, 8]
    # url, port, score
    return data[index]


def delete_proxy(logger, proxy_url, ip):
    # Delete the invalid proxy server.
    try:
        requests.get(proxy_url + '/delete?ip=' + ip)
    except:
        print 'Connect proxy server error!'
        logger.error('Connect proxy server error!')
