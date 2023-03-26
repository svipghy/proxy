#!/usr/bin/python3
# -*- coding: utf-8 -*

import requests
import json

# 替换成你的glados账号cookie
cookie = 'xxxxxxx'
# webhook为你的钉钉机器人的webhook地址
webhook = 'xxxxxxx'

def main():
    checkin_res = checkin()
    if checkin_res == "Please Try Tomorrow":
        print("签到失败，请明天再试！")
    else:
        state_res = get_state()
        content = f'高宏宇,当前天数：{state_res} \n签到结果：{checkin_res}'
        send_dingtalk(content)

def checkin():
    url = 'https://glados.rocks/api/user/checkin'
    headers = {
        'cookie': cookie,
        'origin': 'https://glados.rocks',
        'referer': 'https://glados.rocks/console/checkin',
        'content-type': 'application/json;charset=UTF-8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
    }
    data = {"token": "glados.network"}
    res = requests.post(url, headers=headers, data=json.dumps(data))
    return json.loads(res.text)['message']

def get_state():
    url = 'https://glados.rocks/api/user/status'
    headers = {
        'cookie': cookie,
        'origin': 'https://glados.rocks',
        'referer': 'https://glados.rocks/console/checkin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
    }
    res = requests.get(url, headers=headers)
    return str(json.loads(res.text)['data']['leftDays']).split('.')[0]

def send_dingtalk(content):
    headers = {
        'Content-Type': 'application/json;charset=utf-8'
    }
    data = {
        "msgtype": "text",
        "text": {"content": content}
    }
    res = requests.post(url=webhook, headers=headers, data=json.dumps(data))
    print(res.text)

if __name__ == '__main__':
    main()
