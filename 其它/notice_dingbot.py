# -*- coding: utf-8 -*-
import json
import os.path
import time
import hmac
import base64
import hashlib
import requests
import configparser
import urllib.parse

# 功能：钉钉告警机器人提醒
# 调用时直接使用 dingbot_notice("告警内容")

# 读取钉钉机器人的两个密钥
config = configparser.ConfigParser()
config.read(os.path.join('..', 'all_confs.ini'))
api_url = config.get('Dingbot', 'api_url')  # Webhook
api_secret = config.get('Dingbot', 'api_secret')  # 加签


def dingbot_notice(content):
    def get_timestamp_sign():
        timestamp = str(round(time.time() * 1000))
        secret = api_secret
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return timestamp, sign

    def get_signed_url():
        timestamp, sign = get_timestamp_sign()
        webhook = api_url + "&timestamp=" + timestamp + "&sign=" + sign
        return webhook

    webhook = get_signed_url()
    header = {"Content-Type": "application/json", "Charset": "UTF-8"}
    message = {"msgtype": "text", "text": {"content": content}}
    message_json = json.dumps(message)
    requests.post(url=webhook, data=message_json, headers=header).json()
