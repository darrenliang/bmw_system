

# BMW文档

#### - 版本修订记录

| 文档版本 |    修订日期    |  修订人   | 修订说明 |
| :--: | :--------: | :----: | :--: |
| 1.0  | 2018-01-13 | Darren | 环境配置 |

## 1. 通用描述

### 1.1 环境配置

#### 1.1.1 python vritualenv环境安装

```
cd bmw_system  //进入项目路径
sudo pip install virtualenv  //第一次安装需要
virtualenv --python python3 env  //在项目创建一个env的文件夹
source env/bin/activate  //激活env环境，一旦activate最左边会出现(env)的字母
```

#### 1.1.2 安装项目所需package

```
pip install -r requirements.txt
```

#### 1.1.3 数据库创建

```
python manage.py makemigrations bmw
python manage.py migrate

python manage.py createsuperuser
```

#### 1.1.3 本地服务启动

```
python manage.py runserver 8000
```

#### 

## 2. 业务接口

### 2.1 Charger Details接口

下面的api为http://localhost:8000/details/左边表格的内容，把内容解析出来即可

```
GET http://localhost:8000/api/charger/details/
```

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "result": {
        "vchchargerid": "10245006",
        "vchModelID": "Amos_EVG-32N",
        "vchvenderid": "evpower",
        "vchSerialNo": "21509006",
        "vchFirmwareVer": "2",
        "dblAccumlatedPower": 606.3120000000001,
        "dblAccumlatedMinute": 215.0,
        "vchIP": null,
        "vchMac": "0",
        "vchSoket": "GBT",
        "vchstate": "2",
        "intcurrentfeedback": 0,
        "intcurrent": 32,
        "intchargingcurrent": 0,
        "intconsumedenergy": 1,
        "intElapsedTime": 1,
        "intchargingphase": 1,
        "vchcommand": "1",
        "dblmaxcurrent": 32.0,
        "dblmincurrent": 8.0,
        "intMaxPhase": 1
    }
}
```

### 2.2 Charging Record查询接口

下面的api为http://localhost:8000/details/右下角查询的内容，主要逻辑：

1. 选择日期，比如”2015-11-24“，按照YYYY-MM-DD格式
2. 调用下面api得到当天日期的所有列表
3. 填充Record ID 选择列表，使用api返回的：intrecordid
4. 用户选择了指定的Record ID后，填充对应的Charge Code(intchargingcode)
5. 当用户点击”Start"后，弹出一个Modal View用table显示对应的详情

```
GET http://localhost:8000/api/charger/details/
```

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "result": [
        {
            "intrecordid": 1,
            "intchargingcode": 2,
            "vchchargerid": "21509001",
            "dttstartqueue": "2015-11-24T15:09:47",
            "dttstarttime": "2015-11-24T15:09:47",
            "dttfinishtime": "2015-11-26T15:09:47",
            "dttrealfinish": "2015-11-24T15:14:59"
        },
        {
            "intrecordid": 2,
            "intchargingcode": 3,
            "vchchargerid": "21509001",
            "dttstartqueue": "2015-11-24T15:16:24",
            "dttstarttime": "2015-11-24T15:16:24",
            "dttfinishtime": "2015-11-26T15:16:24",
            "dttrealfinish": "2015-11-24T15:21:40"
        },
        {
            "intrecordid": 4,
            "intchargingcode": 10,
            "vchchargerid": "21509005",
            "dttstartqueue": "2015-11-24T16:27:06",
            "dttstarttime": "2015-11-24T16:27:06",
            "dttfinishtime": "2015-11-26T16:27:06",
            "dttrealfinish": "2015-11-24T17:48:11"
        },
        {
            "intrecordid": 5,
            "intchargingcode": 11,
            "vchchargerid": "21509005",
            "dttstartqueue": "2015-11-24T18:00:49",
            "dttstarttime": "2015-11-24T18:00:49",
            "dttfinishtime": "2015-11-24T19:00:49",
            "dttrealfinish": "2015-11-24T19:00:49"
        },
        {
            "intrecordid": 6,
            "intchargingcode": 12,
            "vchchargerid": "21509005",
            "dttstartqueue": "2015-11-24T18:24:10",
            "dttstarttime": "2015-11-24T18:24:10",
            "dttfinishtime": "2015-11-24T19:24:10",
            "dttrealfinish": "2015-11-24T19:24:10"
        },
        {
            "intrecordid": 7,
            "intchargingcode": 69,
            "vchchargerid": "21509007",
            "dttstartqueue": "2015-11-24T19:29:30",
            "dttstarttime": "2015-11-24T19:29:30",
            "dttfinishtime": "2015-11-24T20:29:30",
            "dttrealfinish": "2015-11-24T19:36:46"
        },
        {
            "intrecordid": 8,
            "intchargingcode": 147,
            "vchchargerid": "21509003",
            "dttstartqueue": "2015-11-24T21:21:47",
            "dttstarttime": "2015-11-24T21:21:47",
            "dttfinishtime": "2015-11-24T22:21:47",
            "dttrealfinish": "2015-11-24T21:22:40"
        },
        {
            "intrecordid": 9,
            "intchargingcode": 148,
            "vchchargerid": "21509003",
            "dttstartqueue": "2015-11-24T21:24:21",
            "dttstarttime": "2015-11-24T21:24:21",
            "dttfinishtime": "2015-11-24T22:24:21",
            "dttrealfinish": "2015-11-24T21:29:38"
        },
        {
            "intrecordid": 10,
            "intchargingcode": 149,
            "vchchargerid": "21509003",
            "dttstartqueue": "2015-11-24T21:30:22",
            "dttstarttime": "2015-11-24T21:30:22",
            "dttfinishtime": "2015-11-24T22:30:22",
            "dttrealfinish": "2015-11-24T21:35:44"
        },
        {
            "intrecordid": 11,
            "intchargingcode": 9,
            "vchchargerid": "21509001",
            "dttstartqueue": "2015-11-24T22:28:05",
            "dttstarttime": "2015-11-24T22:28:05",
            "dttfinishtime": "2015-11-26T22:28:05",
            "dttrealfinish": "2015-11-24T22:34:43"
        },
        {
            "intrecordid": 12,
            "intchargingcode": 2,
            "vchchargerid": "21509008",
            "dttstartqueue": "2015-11-24T22:40:08",
            "dttstarttime": "2015-11-24T22:40:08",
            "dttfinishtime": "2015-11-26T22:40:08",
            "dttrealfinish": "2015-11-24T22:44:10"
        },
        {
            "intrecordid": 13,
            "intchargingcode": 3,
            "vchchargerid": "21509008",
            "dttstartqueue": "2015-11-24T22:44:33",
            "dttstarttime": "2015-11-24T22:44:33",
            "dttfinishtime": "2015-11-26T22:44:33",
            "dttrealfinish": "2015-11-24T22:45:19"
        }
    ]
}
```

### 2.3 Details页面中图表数据解析

这个主要用websocket来接收来的信息，你可以打开console看到每3分钟有一条信息，接口解析再聊

