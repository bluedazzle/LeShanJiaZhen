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
POST /area_tel/
```
###**Parameters**
*   area_name(_Required_|string)——地区名
###**Request**
```
{"area_name":"成都"}
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
*   process_by(_Required_|string)——受理地区管理员
*   consumer(_Required_|int)——客户（电话）
*   file(_Optional_|file)——照片
###**Request**
```
{"content":"水管坏了","process_by":"张全蛋","consumer":123456}
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
{'status': 1, 'body': {'content': '霸王防脱','photo':url}}
```


##**刷新费用单详情**




##**根据地理位置获取当前城市与最近服务点**


根据地理位置获取当前城市
刷新城市电话号码*
提交订单*
拉取广告*
刷新费用单详情
发送短信验证码
上传图片*

预约状态
0   已提交
1   已受理
2   已完成
