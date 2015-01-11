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
{"area_id":333}
```
###**Return**
```
{'status': 1, 'body': {'tel': 123456}}
```

##**提交订单（含上传图片）**
```
POST /mkappoint/
```
###**Parameters**
*   content(_Required_|string)——预约内容
*   area_id(_Required_|int)——受理地区
*   consumer(_Required_|int)——客户（电话）
*   file(_Optional_|file)——照片
*   name(_Optional_|string)——客户姓名
*   address(_Optional_|string)——客户住址
###**Request**
```
{"content":"水管坏了","area_id":333,"consumer":123456,"name":"张三","address":"XXX"}
```
###**Return**
```
{'status': 1, 'body': {'pic_url': pic_url}}
```

##**拉取广告**
```
GET /getad/
```
###**Return**
```
{'status': 1, 'body': {'content': 'XXX','photo':url}}
```


##**刷新大类**
```
GET /getcategory/
```
###**Return**
```
{
    "status": 1,
    "body": {
        "1": "水",
        "2": "电",
        "3": "装修"
    }
}
```

##**刷新具体类目**
```
GET /getitem/
```
###**Parameters**
*   id(_Required_|int)——大类编号，效果 http://127.0.0.1:8000/getitem/?category_id=2
###**Return**
```
{
    "status": 1,
    "body": {
        "2": {
            "content": "已布的线路修起来比较麻烦",
            "price": "50元",
            "title": "电线损坏"
        },
        "4": {
            "content": "应对这种情况我们很专业",
            "price": "50元",
            "title": "电线被老鼠咬了"
        },
        "5": {
            "content": "更换各种电灯泡",
            "price": "50元",
            "title": "电灯坏了"
        }
    }
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