#手机客户端

##**STATUS结果码对照表**
|status结果码|状态|
| --------------  | :---: |
|1|成功|
|2|未知错误|
|3|订单状态改变|
|4|密码错误|
|5|超时|
|6|已存在|
|7|不存在|
|9|权限不足|
|11|验证码为空|
|12|验证码错误|
|13|非法操作|

##**刷新城市电话号码**
```
GET /area_tel/
```
###**Parameters**
*   area_id(_Required_|int)——地区编号
###**Request**
```
{"area_id":1}
```
###**Return**
```
{'status': 1, 'body': {'tel': 123456}}
```

##**获取验证码**
```
POST /getverify/
```
###**Parameters**
*   consumer(_Required_|string)——用户电话
###**Request**
```
{"consumer":"15008242734"}
```
###**Return**
```
{'status': 1, 'body': None}
```

##**通过验证码获取token**
```
POST /phoneverify/
```
###**Parameters**
*   consumer(_Required_|string)——用户电话
*   vercode(_Required_|string)——验证码
###**Request**
```
{"consumer":"15008242734","vercode":"123456"}
```
###**Return**
```
{
    "status": 1,
    "body": [
        {
            "token": "bFV2Rm8wMTUwMDgyNDI3MzQ="
        }
    ]
}
```

##**提交预约（含上传图片）**
```
POST /mkappoint/
```
###**Parameters**
*   content(_Required_|string)——预约内容
*   area_id(_Required_|int)——受理地区
*   consumer(_Required_|string)——客户（电话）
*   token(_Required_|string)——号码token
*   file1(_Optional_|file1)——照片1
*   file2(_Optional_|file2)——照片2
*   file3(_Optional_|file3)——照片3
*   file4(_Optional_|file4)——照片4
*   name(_Optional_|string)——客户姓名
*   address(_Optional_|string)——客户住址
###**Request**
```
{"content":"水管坏了","area_id":1,"consumer":15008242734,"name":"张三","address":"XXX"}
```
###**Return**
```
{'status': 1, 'body': Null}
```

##**拉取广告**
```
GET /getad/
```
###**Return**
```
{
    "status": 1,
    "body": [
        {
            "content": "修水管，送福利",
            "photo": "http://127.0.0.1/meizi.jpg"
        },
        {
            "content": "年前搞清洗，爽爽地过年",
            "photo": "http://127.0.0.1/meizi.jpg"
        }
    ]
}
```


##**刷新大类**
```
GET /getcategory/
```
###**Return**
```
{
    "status": 1,
    "body": [
        {
            "category": "水",
            "category_id": 1
        },
        {
            "category": "电",
            "category_id": 2
        },
        {
            "category": "装修",
            "category_id": 3
        }
    ]
}
```

##**刷新具体类目**
```
GET /getitem/
```
###**Parameters**
*   category_id(_Required_|int)——大类编号，效果 http://127.0.0.1:8000/getitem/?category_id=2
###**Return**
```
{
    "status": 1,
    "body": [
        {
            "item_id": 4,
            "content": "应对这种情况我们很专业",
            "price": "50元",
            "title": "电线被老鼠咬了"
        },
        {
            "item_id": 5,
            "content": "更换各种电灯泡",
            "price": "50元",
            "title": "电灯坏了"
        },
        {
            "item_id": 2,
            "content": "已布的线路修起来比较麻烦",
            "price": "50元",
            "title": "电线损坏"
        }
    ]
}
```

##**根据地理位置获取当前城市与最近服务点(返回id)**
```
POST /getnearest/
```
###**Parameters**
*   lat(_Required_|float)——纬度
*   lng(_Required_|float)——经度
###**Request**
```
{"lat":30,"lng":100}
```
###**Return**
```
{"status": 1, "body": {"area_id": 1}}
```


根据地理位置获取当前城市*
刷新城市电话号码*
提交订单*
拉取广告*
刷新费用单详情
发送短信验证码*
上传图片*
地区对应表获取*

预约状态
1   已提交
2   已受理
3   已完成
4   已取消