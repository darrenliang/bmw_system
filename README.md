

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

### 2.1 Http连接

```
{
    "meta": 
    {
    	"code": 1001,
    	"message": "Successfully to connect web-socket"
    },
    "data": 
    {
    	"time":"1504684753.355295"
    }
}
```



