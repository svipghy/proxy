# 签到脚本,签到成功结果，消息推送到钉钉群

> 纯粹是闲的蛋疼瞎搞的,大家凑合用吧~~~

### 执行脚本

```
cat bash.sh

#!/bin/bash

echo "---------GLaDos签到---------------"
# glados签到 https://www.glados.rocks/
/usr/bin/python3 /home/ghy/glados.py

sleep 20

echo "------------TLY签到---------------"
# TLY签到 https://tly.com/
/usr/bin/python3 /home/ghy/tly.py
```

### 定时任务
```
# 定时签到任务
0 9,12,18 * * * /usr/bin/bash /home/ghy/bash.sh >> /home/ghy/log/checkin_$(date +""\%Y-\%m-\%d_\%T"").log 2>&1

# 每隔15天删除30天以上的签到日志文件
* * */15 * *  /usr/bin/find /home/ghy/log/ -mtime +30 -name "*.log" -exec rm -rf {} \;
```

### 安装Python3
```
yum install python3
```

### pip安装request模块
```
pip3 install requests -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com
```

### 查看pip已经安装的模块
```
pip3 list
certifi (2022.12.7)
charset-normalizer (2.0.12)
idna (3.4)
pip (9.0.3)
requests (2.27.1)
setuptools (39.2.0)
urllib3 (1.26.15)
```
