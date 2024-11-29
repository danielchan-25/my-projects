# -*- coding: utf-8 -*-
import os
import json
import socket
import requests
import configparser


# 日期：2024年11月1日
# 功能：将本机IPV6地址，写入 CloudFlare DNS记录中，适用于家里有公网IPV6地址，且绑定域名访问的。
# 需要先在CloudFlare上获取Token、DNS名称、区域ID
# 可以设置每分钟运行一次，检测到IP地址变动后才会写入CloudFlare

class Update_IPV6_Address():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join('..', 'all_confs.ini'))
        self.dns_name = self.config.get('CloudFlare', 'dns_name')  # 就是DNS名称
        self.zone_id = self.config.get('CloudFlare', 'zone_id')  # 区域ID
        self.token = self.config.get('CloudFlare', 'token')  # 右上角账户里面生成

        self.ipv6_file = 'ipv6.log'

        # 测试API是否有效
        # curl -X GET "https://api.cloudflare.com/client/v4/user/tokens/verify" \
        #      -H "Authorization: Bearer token" \
        #      -H "Content-Type:application/json"

    def get_ipv6_address(self):
        ''' 获取本机IPV6地址，判断ip是否更新 '''

        def old_ip():
            with open(self.ipv6_file, 'r') as r:
                return r.read()

        def new_ip():
            try:
                ipv6s = socket.getaddrinfo(socket.gethostname(), 80)
                if ipv6s:
                    return ipv6s[1][-1][0]
            except Exception as e:
                print(e)
                return None

        old_ip, new_ip = old_ip(), new_ip()
        if new_ip != old_ip:
            with open(self.ipv6_file, 'w') as f:
                f.write(new_ip)
            return new_ip
        return

    def get_record_id(self, dns_name, zone_id, token):
        ''' 获取CloudFlare上的 dns_id'''
        url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        resp = requests.get(url, headers=headers)

        if not json.loads(resp.text)['success']:
            return None
        domains = json.loads(resp.text)['result']
        for i in domains:
            if dns_name == i['name']:
                return i['id']
        return None

    def update_dns_record(self, dns_name, zone_id, token, dns_id, ip, proxied=False):
        ''' 更新DNS记录 '''
        url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{dns_id}'
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        payload = {'type': 'AAAA', 'name': dns_name, 'content': ip, 'proxied': proxied}
        resp = requests.put(url, headers=headers, json=payload)
        if not json.loads(resp.text)['success']:
            return None
        return True

    def run(self):
        ip = self.get_ipv6_address()
        if ip:
            dns_id = self.get_record_id(self.dns_name, self.zone_id, self.token)
            if self.update_dns_record(self.dns_name, self.zone_id, self.token, dns_id, ip) is False:
                print('更新失败')


if __name__ == '__main__':
    Update_IPV6_Address().run()
