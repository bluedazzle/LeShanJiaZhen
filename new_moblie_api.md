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
|14|不能兑换自己邀请码|

##**订单状态码对照表**
|status|状态|
| --------------  | :---: |
|1|待处理|
|2|已确认|
|3|配送中|
|4|已完成|
|5|已撤单|

##**优惠券类型对照表**
|type|优惠券|
| --------------  | :---: |
|1|邀请码优惠券|
|2|在线支付优惠券|
|3|游戏优惠券|

##**API HOST**
```
http://www.kuailejujia.com/api/v1/
```

##**注册**
#####注册流程
1、先向consumer/send_reg_verify请求发送验证码验证手机
2、向consumer/verify_reg_code验证收到的验证码
3、请求consumer/register注册成功或失败

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
POST /consumer/verify_reg_code
```
###**Parameters**
* phone(_Required_|string)-用户名，必须为手机号
* verify_code(_Required_|string)-验证码
###**Request**
```
{"phone":"18215606355","verify_code":"123456"}
```
###**Return**
```
{"status": 1, "body": {"msg": "success"}}
or
{"status": 7, "body": {"msg": "verify failed"}}
```
######步骤三：
```
POST /consumer/register
```
###**Parameters**
* username(_Required_|string)-用户名，必须为手机号
* password(_Required_|string)-密码
* address(_Optional_|string)-用户地址
* sex(_Optional_|integer)-用户性别 1男 2女 3保密
* birthday(_Optional_|string)-生日 字符格式 1999-01-01
###**Request**
```
{"username":"18215606355","password":"123456","address":"kb258","sex":1,"birthday":"1999-01-01"}
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
{"username":"18215606355","old_password":"123456","new_password":"123456qq","private_token":"ajhsdflkajshdflashfdkjshf"}
```
###**Return**
```
{"status": 1, "body": {"msg": "change password success"}}
or
{"status": 13, "body": {"msg": "login first before other action"}}
```

##**登陆**

#####顾客登陆
```
POST /consumer/login
```
###**Parameters**
* username(_Required_|string)-用户名，必须为手机号
* password(_Required_|string)-用户密码
###**Request**
```
{"username":"18215606355","password":"123456"}
```
###**Return**
```
{"status": 1, "body": {"msg": "login success", "username": "18215606355", "private_token": "ztVrCqRAOSP3GQI=vWx5hHDokBsNcT1J"}}
or
{"status": 4, "body": {"msg": "password is not right"}}
```


##**登出**

#####顾客注销
```
POST /consumer/logout
```
###**Parameters**
* username(_Required_|string)-用户名，必须为手机号
* private_token(_Required_|string)-用户token
###**Request**
```
{"username":"18215606355","private_token":"123456"}
```
###**Return**
```
{"status": 1, "body": {"msg": "log out success"}}
or
{"status": 13, "body": {"msg": "login first before other action"}}
```

##**忘记密码**

#####顾客忘记密码
#####忘记密码流程：
1、/consumer/forget_password请求验证码
2、/consumer/reset_password重置密码
######步骤一：

```
POST /consumer/forget_password
```
###**Parameters**
* phone(_Required_|string)-用户手机号
###**Request**
```
{"phone":"18215606355"}
```
###**Return**
```
{"status": 1, "body": {"test": {"verify_code": "601532", "success": true}, "msg": "verify code send success"}}
or
{"status": 7, "body": {"msg": "account does not exist, please sign up"}}
```

######步骤二：

```
POST /consumer/reset_password
```
###**Parameters**
* phone(_Required_|string)-用户手机号
* verify_code(required_|string)-验证码
* new_password(required_|string)-新密码
###**Request**
```
{"phone":"18215606355","verify_code":"123456","new_password":"123456"}
```
###**Return**
```
{"status": 1, "body": {"username": "18215606355", "msg": "reset password success", "private_token": "AIgJd=zWNsiZcPayqLjfk20Ox6Bb57Dt"}}
or
{"status": 12, "body": {"msg": "verify code does not exist"}}
```

##**获取安卓版本号**

#####获取最新安卓版本号
```
GET /consumer/get_android_version
```

###**Return**
```
{"status": 1, "body": {"update_time": "2015-03-13 19:47:06+08:00", "android_version": "2.1.6"}}
or
{"status": 7, "body": {"msg": "no available version info"}}
```

##**获取苹果版本号**

#####获取最新苹果版本号
```
GET /consumer/get_ios_version
```

###**Return**
```
{"status": 1, "body": {"update_time": "2015-03-13 19:47:06+08:00", "ios_version": "2.1.6"}}
or
{"status": 7, "body": {"msg": "no available version info"}}
```

##**获取消息**

#####顾客获取消息中心消息
```
POST /consumer/get_messages
```
###**Parameters**
* username(_Required_|string)-用户名，必须为手机号
* private_token(_Required_|string)-用户token
###**Request**
```
{"username":"18215606355","private_token":"123456"}
```
###**Return**
```
{"status": 1, "body": {"messages": [{"content": "djdjdjd", "create_time": "2015-03-13 19:55:20.679150+08:00", "deadline": "2015-03-13 19:55:17+08:00"}, {"content": "\u5316\u971c\u5b9a\u65f6\u5668\uff08100L\u5185\uff09", "create_time": "2015-03-13 19:55:07.647434+08:00", "deadline": "2015-03-13 19:54:59+08:00"}]}}
or
{"status": 13, "body": {"msg": "login first before other action"}}
```

##**获取优惠券**

#####顾客获取优惠券
```
POST /consumer/get_coupons
```
###**Parameters**
* username(_Required_|string)-用户名，必须为手机号
* private_token(_Required_|string)-用户token
###**Request**
```
{"username":"18215606355","private_token":"123456"}
```
###**Return**
```
{"status": 1, "body": {"coupons": [{"owned_time": "2015-03-13 20:14:22+08:00", "create_time": "2015-03-13 20:14:25.308127+08:00", "cou_id": "20102102", "deadline": "2015-03-13 20:06:30+08:00", "type": 1, "value": 5, "if_use": false}, {"owned_time": "2015-03-13 20:14:14+08:00", "create_time": "2015-03-13 20:14:16.314338+08:00", "cou_id": "20102101", "deadline": "2015-03-13 20:06:51+08:00", "type": 2, "value": 13, "if_use": false}, {"owned_time": "2015-03-13 20:14:08+08:00", "create_time": "2015-03-13 20:14:09.464093+08:00", "cou_id": "20102105", "deadline": "2015-03-13 20:07:06+08:00", "type": 1, "value": 5, "if_use": true}]}}
or
{"status": 13, "body": {"msg": "login first before other action"}}
```

##**获取优惠券**

#####顾客获取优惠券
```
POST /consumer/new_feedback
```
###**Parameters**
* phone(_Required_|string)-用户手机号
* content(_Required_|string)-反馈内容
###**Request**
```
{"phone":"18215606355","content":"test"}
```
###**Return**
```
{"status": 1, "body": {"msg": "feedback add success"}}
```

##**定位当前城市**

#####顾客定位当前所在城市
```
POST /consumer/city_search
```
###**Parameters**
* city_num(_Required_|string)-城市统一编码
###**Request**
```
{"city_num":"513012"}
```
###**Return**
```
{"status": 1, "body": {"msg": "get city success", "city": {"city_num": "511100", "city_name": "\u56db\u5ddd\u7701\u4e50\u5c71\u5e02", "city_address": "\u56db\u5ddd\u7701\u4e50\u5c71\u5e02\u4e00\u5768\u7fd4\u522b\u5885", "city_info": "\u56db\u5ddd\u7701\u4e50\u5c71\u5e02\u4e00\u5768\u7fd4\u522b\u5885", "city_tel": "61830000"}, "match": true}}
or
{"status": 1, "body": {"msg": "match resemble city success", "city": {"city_num": "511100", "city_name": "\u56db\u5ddd\u7701\u4e50\u5c71\u5e02", "city_address": "\u56db\u5ddd\u7701\u4e50\u5c71\u5e02\u4e00\u5768\u7fd4\u522b\u5885", "city_info": "\u56db\u5ddd\u7701\u4e50\u5c71\u5e02\u4e00\u5768\u7fd4\u522b\u5885", "city_tel": "61830000"}, "match": false}}
```

##**更改个人信息**

#####顾客更改个人信息
```
POST /consumer/change_info
```
###**Parameters**
* username(_Required_|string)-用户名，必须为手机号
* private_token(_Required_|string)-token
* address(_Optional_|string)-用户地址
* sex(_Optional_|integer)-用户性别 1男 2女 3保密
* birthday(_Optional_|string)-生日 字符格式 1999-01-01
###**Request**
```
{"username":"18215606355","private_token":"asdfasdfasqwe56","address":"kb258","sex":1,"birthday":"1999-01-01"}
```
###**Return**
```
{"status": 1, "body": {"msg": "change info success"}}
or
{"status": 13, "body": {"msg": "login first before other action"}}
```


##**兑换邀请码优惠券**

#####顾客兑换邀请码优惠券
```
POST /consumer/get_invite_coupon
```
###**Parameters**
* username(_Required_|string)-用户名，必须为手机号
* private_token(_Required_|string)-token
* invite_code(_Required|string)-邀请码
###**Request**
```
{"username":"18215606355","private_token":"asdfasdfasqwe56","invite_code":"123455"}
```
###**Return**
```
{"status": 1, "body": {"msg": "invite code exchange success"}}
or
{"status": 6, "body": {"msg": "you have exchanged this invite code"}}
or
{"status": 7, "body": {"msg": "no invite code info"}}
or
{"status": 14, "body": {"msg": "you can not exchange your own invite code"}}
```
