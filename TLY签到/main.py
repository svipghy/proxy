import time
import requests
import base64
import json

cookie = "xxxxxx"
token = 'xxxxxx'  # 验证码token

# token在http://www.bhshare.cn/imgcode/gettoken/ 自行申请

# 钉钉机器人Webhook URL
webhook_url = "xxxxxxx"


def imgcode_online(imgurl):
    data = {"token": token, "type": "online", "uri": imgurl}
    response = requests.post("http://www.bhshare.cn/imgcode/", data=data)
    result = json.loads(response.text)
    return result["data"] if result["code"] == 200 else "error"


def getmidstring(html, start_str, end):
    start = html.find(start_str) + len(start_str)
    end = html.find(end, start)
    return html[start:end].strip() if start >= len(start_str) and end >= 0 else ""


def tly():
    sign_url = "https://tly30.com/modules/index.php"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        "Cookie": cookie}
    response = requests.get(url=sign_url, headers=header)
    signtime = getmidstring(response.text, '<p>上次签到时间：<code>', '</code></p>')
    timeArray = time.strptime(signtime, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    t = int(time.time())
    if t - timeStamp > 86400:
        print("距上次签到时间大于24小时啦,可签到")
        done = False
        while not done:
            captcha_url = "https://tly30.com/other/captcha.php"
            sign_url = f"https://tly30.com/modules/_checkin.php?captcha={imgcode_online('data:image/jpeg;base64,' + str(base64.b64encode(requests.get(captcha_url, headers=header).content), 'utf-8')).upper()}"
            response = requests.get(url=sign_url, headers=header)
            print(response.text)
            if "流量" in response.text:
                done = True

                # 签到成功后发送钉钉消息
                result = "TLY 签到成功啦！"
                message = {
                    "msgtype": "text",
                    "text": {
                        "content": result
                    }
                }
                requests.post(webhook_url, json=message)

            else:
                done = False
                print("未签到成功，沉睡3秒再来一次")
                time.sleep(3)
        return result
    else:
        print("还未到时间！", t - timeStamp)
        return "还未到签到时间！"


if __name__ == "__main__":
    result = tly()
    print(result)
