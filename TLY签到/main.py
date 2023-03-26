#!/usr/bin/python3
# -*- coding: utf-8 -*

import time
import requests
import base64
import json

COOKIE = "xxxxxx"

# token在http://www.bhshare.cn/imgcode/gettoken/ 自行申请
TOKEN = 'xxxxxx'

# 钉钉机器人Webhook URL
WEBHOOK_URL = "xxxxxxx"

def imgcode_online(imgurl):
    data = {"token": TOKEN, "type": "online", "uri": imgurl}
    response = requests.post("http://www.bhshare.cn/imgcode/", data=data)
    result = json.loads(response.text)
    return result["data"] if result["code"] == 200 else "error"

def get_last_sign_time():
    sign_url = "https://tly30.com/modules/index.php"
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36", "Cookie": COOKIE}
    response = requests.get(url=sign_url, headers=header)
    signtime = get_mid_string(response.text, '<p>上次签到时间：<code>', '</code></p>')
    timeArray = time.strptime(signtime, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp

def sign():
    sign_url = "https://tly30.com/modules/_checkin.php"
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36", "Cookie": COOKIE}
    last_sign_time = get_last_sign_time()
    t = int(time.time())
    if t - last_sign_time > 86400:
        print("距上次签到时间大于24小时啦，可以签到")
        done = False
        while not done:
            captcha_url = "https://tly30.com/other/captcha.php"
            sign_url_with_captcha = f"{sign_url}?captcha={imgcode_online('data:image/jpeg;base64,' + str(base64.b64encode(requests.get(captcha_url, headers=header).content), 'utf-8')).upper()}"
            response = requests.get(url=sign_url_with_captcha, headers=header)
            print(response.text)
            if "流量" in response.text:
                done = True
                return "TLY 签到成功啦！"
            else:
                done = False
                print("未签到成功，沉睡3秒再来一次")
                time.sleep(3)
        return result
    else:
        print("还未到时间！", t - last_sign_time)
        return "还未到签到时间！"

def send_dd_message(result):
    message = {"msgtype": "text", "text": {"content": result}}
    requests.post(WEBHOOK_URL, json=message)

if __name__ == "__main__":
    result = sign()
    print(result)
    if "成功" in result:
        send_dd_message(result)
