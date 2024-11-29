# -*- coding: utf-8 -*-
import argparse
import requests

# 日期：2024年11月1日
# 功能：推送消息至Bark客户端
# API文档：https://github.com/Finb/bark-server/blob/master/docs/API_V2.md


url = 'http://192.168.2.11:8402/push'  # Bark-Server
headers = {'Content-Type': 'application/json', 'charset': 'utf-8'}


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--title', type=str, help='标题')
    parser.add_argument('--body', type=str, help='内容')
    parser.add_argument('--device_key', type=str, help='设备key')
    parser.add_argument('--group', type=str, help='分组')
    args = parser.parse_args()

    payload = {
        'title': args.title,
        'body': args.body,
        'category': "0",
        'device_key': args.device_key,
        'level': 'active',
        'badge': 1,
        'automaticallyCopy': 1,
        'group': args.group
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")


if __name__ == '__main__':
    main()
