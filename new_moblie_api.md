#家政手机客户端

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

##**订单状态码对照表**
|status|状态|
| --------------  | :---: |
|1|待处理|
|2|已确认|
|3|配送中|
|4|已完成|
|5|已撤单|


##**注册**
#####注册流程
1、先向consumer/send_reg_verify请求发送验证码验证手机
2、请求consumer/register注册成功或失败

#####顾客注册
######步骤一：
```
POST /consumer/send_reg_verify
```
###**Parameters**
* phone(_Required_|string)-用户名，必须为手机号
###**Request**
```
{"phone":18215606355}
```
###**Return**
```
{"status": 1, "body": {"verify_code": "209467", "success": true}}
or
{"status":2,"body":null}
```

######步骤二：
```
POST /consumer/register
```
###**Parameters**
* username(_Required_|string)-用户名，必须为手机号
* password(_Required_|string)-密码
* verify_code(_Required_|string)-验证码
* address(_Optional_|string)-用户地址
* sex(_Optional_|integer)-用户性别 1男 2女 3保密
* birthday(_Optional_|string)-生日 字符格式 1999-01-01
###**Request**
```
{"username":"18215606355","password":"123456","verify_code":"123456","address":"kb258","sex":1,"birthday":"1999-01-01"}
```
###**Return**
```
{"status": 1, "body": {"msg": "register success", "phone": "18215606354", "private_token": "UL1qcJIgsiaNAzPnSe+fjQ9DBX=x8yhG"}}
or
{"status": 6, "body": {"msg": "username has exist"}}
```

##**更改密码**

#####顾客更改密码
```
POST /consumer/change_password
```
###**Parameters**
* username(_Required_|string)-用户名，必须为手机号
* private_token(_Required_|string)-用户token
* old_password(_Required_|string)-用户原密码
* new_password(_Required_|string)-用户新密码
###**Request**
```
{"username":"18215606355",}
```
###**Return**
```
{"status": 1, "body": {"verify_code": "209467", "success": true}}
or
{"status":2,"body":null}
```

##**商品**

#####获取商品列表
```
POST /consumer/get_goods_item
```
###**Parameters**
* city_number(_Required_|string)-城市统一编码
###**Request**
```
{"city_number":"511000"}
```
###**Return**
```
{"status": 1, "body": {"msg": "goods_p get success", "goods_item": [{"item_name": "\u51b0\u7bb1\u7ef4\u4fee", "have_advertisment": false, "advertisment": ""}, {"item_name": "\u6c34\u7ef4\u4fee", "have_advertisment": false, "advertisment": ""}]}}
or
{"status": 7, "body": {"msg": "invalid city number"}}
```

##**商品**

#####获取商品详细
```
POST /consumer/get_goods_detail
```
###**Parameters**
* pid(_Required_|string)-父商品id
###**Request**
```
{"pid":"5"}
```
###**Return**
```
{"status": 1, "body": {"msg": "goods detail get success", "goods": [{"item_name": "\u7acb\u5f0f\u51b0\u7bb1\u7ef4\u4fee", "s_item_list": [{"picture": "c:/ss/ss.jpg", "title": "\u561f\u561f", "repair_price": 2.0, "made_by": "\u7684", "material": "\u7684", "made_in": "\u5f53\u65f6", "real_price": 10.0, "plus": "\u53d1", "sid": 5, "content": "\u65b9\u6cd5", "origin_price": 10.0, "brand": "\u7684"}], "oid": 3}, {"item_name": "\u51b0\u67dc\u7ef4\u4fee", "s_item_list": [], "oid": 4}], "pid": 2}}
or
{"status": 7, "body": {"msg": "invalid id"}}
```


