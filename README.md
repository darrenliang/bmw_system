

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

### 2.4 Basic Settings数值显示接口

这个api需要在http://localhost:8000/settings/ 页面解析，进入此页面把所有元素显示在输入框初始化。

Request:

```
GET http://localhost:8000/api/basic/settings/
```

Response:


```
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "vchcardreadercom": "Com10",
    "yeainstallyear": "2013",
    "intinstallmonth": 100,
    "blncurrentdistribution": 1,
    "vchpowermetercom": "Com4",
    "vchpowersequence": "ABC",
    "intcurrency": 86,
    "dblchargingdeductionpower": 3.0,
    "intchargingdeductionminute": 120,
    "intdeductionprioritypower": 2,
    "intdeductionpriorityminute": 1,
    "dblpowercoefficient": 0.001,
    "blninternaltesting": 1,
    "intmaxcurrenta": 32,
    "intmaxcurrentb": 32,
    "intmaxcurrentc": 32
}
```

### 2.5 Basic Settings数值更新接口

这个api需要在http://localhost:8000/settings/ 页面更新，注意为post并附带参数，需要在前端做javascript的检测。

Request:

```
POST http://localhost:8000/api/basic/settings/
```

|         Parameter          |  Type  | Description |
| :------------------------: | :----: | :---------: |
|      vchcardreadercom      | string |             |
|       yeainstallyear       | string |             |
|      intinstallmonth       |  int   |             |
|   blncurrentdistribution   |  int   |             |
|      vchpowermetercom      | string |             |
|      vchpowersequence      | string |             |
|        intcurrency         |  int   |             |
| dblchargingdeductionpower  | float  |             |
| intchargingdeductionminute |  int   |             |
| intdeductionprioritypower  |  int   |             |
| intdeductionpriorityminute |  int   |             |
|    dblpowercoefficient     | float  |             |
|     blninternaltesting     |  int   |             |
|       intmaxcurrenta       |  int   |             |
|       intmaxcurrentb       |  int   |             |
|       intmaxcurrentc       |  int   |             |

Response:

```
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "vchcardreadercom": "Com10",
    "yeainstallyear": "2013",
    "intinstallmonth": 100,
    "blncurrentdistribution": 1,
    "vchpowermetercom": "Com4",
    "vchpowersequence": "ABC",
    "intcurrency": 86,
    "dblchargingdeductionpower": 3.0,
    "intchargingdeductionminute": 120,
    "intdeductionprioritypower": 2,
    "intdeductionpriorityminute": 1,
    "dblpowercoefficient": 0.001,
    "blninternaltesting": 1,
    "intmaxcurrenta": 32,
    "intmaxcurrentb": 32,
    "intmaxcurrentc": 32
}
```

### 2.6 Charger Info数量统计接口

这个api需要在http://localhost:8000/overview/ 页面解析，进入此页面可以看到电桩总数、总充电电量、总充电次数、正在使用，通过下面api进行解析填充。

Request:

```
GET http://localhost:8000/api/charger/info/statistic/
```

Response:

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "total_charger": 13,  //电桩总数
    "accumulate_power": 12214.54,  //总充电电量
    "accumulate_minutes": 4230.0,  //总充电次数
    "total_charging": 0  //正在使用
}
```

### 2.7 充电记录总览接口

这个api需要在http://localhost:8000/overview/ 页面解析，可以看到充电记录总览的表格，对内容进行填充，新增num，为要显示的记录个数，默认情况下不需要传，系统默认。

Request:

```
GET http://localhost:8000/api/recent/charging/record/list/
```

| Parameter | Type | Description |
| :-------: | :--: | :---------: |
|    num    | int  |             |

Response:

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "num": 7,
    "result": [
        {
            "intrecordid": 1406,
            "dttfinishtime": "2016-11-25 14:11:55",
            "dblenergy": 2.458
        },
        {
            "intrecordid": 1405,
            "dttfinishtime": "2016-11-25 13:06:59",
            "dblenergy": 2.38
        },
        {
            "intrecordid": 1404,
            "dttfinishtime": "2016-11-24 18:29:26",
            "dblenergy": 1.024
        },
        {
            "intrecordid": 1403,
            "dttfinishtime": "2016-11-18 11:26:32",
            "dblenergy": 5.496
        },
        {
            "intrecordid": 1402,
            "dttfinishtime": "2016-11-18 09:39:54",
            "dblenergy": 6.75
        },
        {
            "intrecordid": 1401,
            "dttfinishtime": "2016-11-18 09:09:27",
            "dblenergy": 6.006
        },
        {
            "intrecordid": 1400,
            "dttfinishtime": "2016-11-18 08:55:00",
            "dblenergy": 0.545
        }
    ]
}
```

### 2.8 电桩总览接口

这个api需要在http://localhost:8000/overview/ 页面解析，可以看到电桩总览的表格，对内容进行填充。

Request:

```
GET http://localhost:8000/api/recent/charger/state/list/
```

Response:

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "result": [
        {
            "vchchargerid": "60303001",
            "vchstate": "BootUp",
            "vchcommand": "BootNotification"
        },
        {
            "vchchargerid": "21509003",
            "vchstate": "bootup",
            "vchcommand": "1"
        },
        {
            "vchchargerid": "21509002",
            "vchstate": "bootup",
            "vchcommand": "1"
        },
        {
            "vchchargerid": "21509001",
            "vchstate": "bootup",
            "vchcommand": "1"
        },
        {
            "vchchargerid": "10245008",
            "vchstate": "2",
            "vchcommand": "1"
        },
        {
            "vchchargerid": "10245007",
            "vchstate": "2",
            "vchcommand": "1"
        },
        {
            "vchchargerid": "10245006",
            "vchstate": "2",
            "vchcommand": "1"
        },
        {
            "vchchargerid": "10245005",
            "vchstate": "15",
            "vchcommand": "1"
        },
        {
            "vchchargerid": "10245004",
            "vchstate": "2",
            "vchcommand": "1"
        },
        {
            "vchchargerid": "10245003",
            "vchstate": "2",
            "vchcommand": "1"
        }
    ]
}
```

### 2.9 联网状态总览接口

这个api需要在http://localhost:8000/overview/ 页面解析，可以看到联网状态总览，对内容进行填充。

Request:

```
GET http://localhost:8000/api/charger/state/statistic/
```

Response:

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "result": [
        {
            "BootUp": 38.46  //数值类型为百分比，所有状态加起来等于100
        },
        {
            "Available": 0.0
        },
        {
            "PreParing": 0.0
        },
        {
            "Charging": 0.0
        },
        {
            "StatusChanged": 0.0
        },
        {
            "StopCharging": 0.0
        },
        {
            "RemoteCharging": 0.0
        },
        {
            "RemoteStopCharging": 0.0
        },
        {
            "SendMessage": 0.0
        },
        {
            "Updating": 0.0
        },
        {
            "Unavailable": 0.0
        },
        {
            "Reboot": 0.0
        },
        {
            "Faulted": 0.0
        },
        {
            "SupsendedEV": 0.0
        },
        {
            "Finishing": 0.0
        },
        {
            "Other": 61.54
        }
    ]
}
```

### 2.10 总电量变化

这个api需要在http://localhost:8000/overview/ 页面解析，没有参数的为（默认）：http://localhost:8000/api/monthly/energy/， 输入参数（会有一个charger_id list 的api）：http://localhost:8000/api/monthly/energy/?charger_id=21509005，横坐标格式为yyyy-mm，charger_id的api参考下一个接口

Request:

```
GET http://localhost:8000/api/monthly/energy/
```

Response:

```
HTTP 200 OK
Allow: GET, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "x": [
        "2015-12",
        "2015-11",
        "2015-10",
        "2015-09",
        "2015-08",
        "2015-07"
    ],
    "y": [
        60.93099999999999,
        91.87100000000004,
        0,
        0,
        0,
        0
    ]
}
```

### 2.11 电池电量变化

这个api需要在http://localhost:8000/overview/ 页面解析，当用户选择了radio button中的电池电量变化所调用

Request:

```
GET http://localhost:8000/api/monthly/energy/list/
```

Response:

```
HTTP 200 OK
Allow: OPTIONS, GET
Content-Type: application/json
Vary: Accept

{
    "data": [
        {
            "charger_id": "21509001",
            "y": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                15.475000000000001,
                11.071
            ],
            "x": [
                "2015-01",
                "2015-02",
                "2015-03",
                "2015-04",
                "2015-05",
                "2015-06",
                "2015-07",
                "2015-08",
                "2015-09",
                "2015-10",
                "2015-11",
                "2015-12"
            ]
        },
        {
            "charger_id": "21509002",
            "y": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                6.183,
                0
            ],
            "x": [
                "2015-01",
                "2015-02",
                "2015-03",
                "2015-04",
                "2015-05",
                "2015-06",
                "2015-07",
                "2015-08",
                "2015-09",
                "2015-10",
                "2015-11",
                "2015-12"
            ]
        },
        {
            "charger_id": "21509003",
            "y": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                7.199999999999999,
                0.007
            ],
            "x": [
                "2015-01",
                "2015-02",
                "2015-03",
                "2015-04",
                "2015-05",
                "2015-06",
                "2015-07",
                "2015-08",
                "2015-09",
                "2015-10",
                "2015-11",
                "2015-12"
            ]
        },
        {
            "charger_id": "21509004",
            "y": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                13.309,
                12.598
            ],
            "x": [
                "2015-01",
                "2015-02",
                "2015-03",
                "2015-04",
                "2015-05",
                "2015-06",
                "2015-07",
                "2015-08",
                "2015-09",
                "2015-10",
                "2015-11",
                "2015-12"
            ]
        },
        {
            "charger_id": "21509005",
            "y": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                12.107000000000003,
                12.532
            ],
            "x": [
                "2015-01",
                "2015-02",
                "2015-03",
                "2015-04",
                "2015-05",
                "2015-06",
                "2015-07",
                "2015-08",
                "2015-09",
                "2015-10",
                "2015-11",
                "2015-12"
            ]
        },
        {
            "charger_id": "21509006",
            "y": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                20.298999999999996,
                13.451
            ],
            "x": [
                "2015-01",
                "2015-02",
                "2015-03",
                "2015-04",
                "2015-05",
                "2015-06",
                "2015-07",
                "2015-08",
                "2015-09",
                "2015-10",
                "2015-11",
                "2015-12"
            ]
        },
        {
            "charger_id": "21509007",
            "y": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                8.675999999999998,
                0.25
            ],
            "x": [
                "2015-01",
                "2015-02",
                "2015-03",
                "2015-04",
                "2015-05",
                "2015-06",
                "2015-07",
                "2015-08",
                "2015-09",
                "2015-10",
                "2015-11",
                "2015-12"
            ]
        },
        {
            "charger_id": "21509008",
            "y": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                8.622,
                11.022
            ],
            "x": [
                "2015-01",
                "2015-02",
                "2015-03",
                "2015-04",
                "2015-05",
                "2015-06",
                "2015-07",
                "2015-08",
                "2015-09",
                "2015-10",
                "2015-11",
                "2015-12"
            ]
        }
    ]
}
```

### 2.12 充电ID列表

暂时用id=21509005去测试

Request:

```
GET http://localhost:8000/api/charger/id/list/
```

Response:

```
HTTP 200 OK
Allow: GET, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "chargers": [
        "00504001",
        "10245001",
        "10245002",
        "10245003",
        "10245004",
        "10245005",
        "10245006",
        "10245007",
        "10245008",
        "21509001",
        "21509002",
        "21509003",
        "21509004",
        "21509005",
        "21509006",
        "21509007",
        "21509008",
        "60303001"
    ]
}
```

### 2.13 相位仪表图

这个api需要在http://localhost:8000/overview/ 页面解析，右边的3个相位数值

Request:

```
GET http://localhost:8000/api/max/current/list/
```

Response:

```
HTTP 200 OK
Allow: GET, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "int_max_current_a": 32,
    "int_max_current_b": 32,
    "int_max_current_c": 32
}
```

### 2.14 点位电装列表

这个api需要在http://localhost:8000/devices/ 页面解析，最下面的列表，保留最右边操作命令，左边的列表表示为如下参数列表的4个参数Charger ID（电桩ID）、Firmware Ver（固件版本）、Model ID（固件ID）、State（状态），列表名字用中英文表示

Request:

```
GET http://localhost:8000/api/charger/list/
```

Response:

```
HTTP 200 OK
Allow: GET, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "data": [
        {
            "vch_charger_id": "00504001",
            "vch_firmware_ver": "271015 ",
            "vch_model_id": "",
            "vch_state": "BootUp"
        },
        {
            "vch_charger_id": "60303001",
            "vch_firmware_ver": "HKMB19167 ",
            "vch_model_id": "",
            "vch_state": "BootUp"
        },
        {
            "vch_charger_id": "10245001",
            "vch_firmware_ver": "",
            "vch_model_id": "EVC32N",
            "vch_state": "hahaha"
        },
        {
            "vch_charger_id": "10245002",
            "vch_firmware_ver": "2",
            "vch_model_id": "Amos_EVG-32N",
            "vch_state": "2"
        },
        {
            "vch_charger_id": "10245003",
            "vch_firmware_ver": "2",
            "vch_model_id": "Amos_EVG-32N",
            "vch_state": "2"
        },
        {
            "vch_charger_id": "10245005",
            "vch_firmware_ver": "2",
            "vch_model_id": "Amos_EVG-32N",
            "vch_state": "15"
        },
        {
            "vch_charger_id": "10245006",
            "vch_firmware_ver": "2",
            "vch_model_id": "Amos_EVG-32N",
            "vch_state": "2"
        },
        {
            "vch_charger_id": "10245007",
            "vch_firmware_ver": "2",
            "vch_model_id": "Amos_EVG-32N",
            "vch_state": "2"
        },
        {
            "vch_charger_id": "10245008",
            "vch_firmware_ver": "2",
            "vch_model_id": "Amos_EVG-32N",
            "vch_state": "2"
        },
        {
            "vch_charger_id": "10245004",
            "vch_firmware_ver": "2",
            "vch_model_id": "Amos_EVG-32N",
            "vch_state": "2"
        },
        {
            "vch_charger_id": "21509001",
            "vch_firmware_ver": "2",
            "vch_model_id": "Amos_EVG-32N",
            "vch_state": "bootup"
        },
        {
            "vch_charger_id": "21509002",
            "vch_firmware_ver": "2",
            "vch_model_id": "Amos_EVG-32N",
            "vch_state": "bootup"
        },
        {
            "vch_charger_id": "21509003",
            "vch_firmware_ver": "2",
            "vch_model_id": "Amos_EVG-32N",
            "vch_state": "bootup"
        },
        {
            "vch_charger_id": "21509004",
            "vch_firmware_ver": "2",
            "vch_model_id": "Amos_EVG-32N",
            "vch_state": null
        },
        {
            "vch_charger_id": "21509005",
            "vch_firmware_ver": "2",
            "vch_model_id": "Amos_EVG-32N",
            "vch_state": null
        },
        {
            "vch_charger_id": "21509006",
            "vch_firmware_ver": "2",
            "vch_model_id": "Amos_EVG-32N",
            "vch_state": null
        },
        {
            "vch_charger_id": "21509007",
            "vch_firmware_ver": "2",
            "vch_model_id": "Amos_EVG-32N",
            "vch_state": null
        },
        {
            "vch_charger_id": "21509008",
            "vch_firmware_ver": "2",
            "vch_model_id": "Amos_EVG-32N",
            "vch_state": null
        }
    ]
}
```

### 



## 3. 图表接口

### 3.1 总电量趋势变化接口

和原来的总电量趋势变化接口几乎一样，传入参数有所不同

Request:

```
GET http://localhost:8000/bmw/chart/getAllRecentChargerRecords/
```

| Parameter  |  Type  |         Description          |
| :--------: | :----: | :--------------------------: |
|    mode    |  int   | 1-Yearly，2-Monthly，3-Daily |
| charger_id | string |             可选             |
|   offset   |  int   |        最近几年/月/日        |

Response:

```
{
    "x": [
        "2018-07",
        "2018-08",
        "2018-09",
        "2018-10",
        "2018-11",
        "2018-12",
        "2019-01",
        "2019-02",
        "2019-03",
        "2019-04",
        "2019-05",
        "2019-06"
    ],
    "y": [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        3826.0,
        4056.0,
        0.0,
        0.0,
        0.0
    ],
    "total": 7882.0
}

```



### 3.2 电桩充电量变化接口

和原来的电桩充电量变化接口几乎一样，返回参数format有所不同，外面少包了一层data

Request:

```
GET http://localhost:8000/bmw/chart/getRecentChargerRecords
```

| Parameter | Type |         Description          |
| :-------: | :--: | :--------------------------: |
|   mode    | int  | 1-Yearly，2-Monthly，3-Daily |
|  offset   | int  |        最近几年/月/日        |

Response:

```
[
    {
        "charger_id": "05010210",
        "x": [
            "2018-07",
            "2018-08",
            "2018-09",
            "2018-10",
            "2018-11",
            "2018-12",
            "2019-01",
            "2019-02",
            "2019-03",
            "2019-04",
            "2019-05",
            "2019-06"
        ],
        "y": [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            3826.0,
            4056.0,
            0.0,
            0.0,
            0.0
        ],
        "total": 7882.0
    }
]
```



























