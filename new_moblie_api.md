#家政手机客户端

##**STATUS结果码对照表**
|status结果码|状态|
| --------------  | :---: |
|0|失败|
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
|20|金额不正确|
|21|优惠券使用失败|

##**订单状态码对照表**
|status|状态|
| --------------  | :---: |
|1|待处理|
|2|已确认|
|3|配送中|
|4|已完成|
|5|已撤单|
|6|已评价|

##**优惠券码对照表**
|status|状态|
| --------------  | :---: |
|1|好友邀请|
|2|在线支付|
|3|游戏获取|
|4|注册|
|5|系统赠送|


##**广告url码说明**
```
first_jump
```
|code|含义|
| --------------  | :---: |
|1|首页|
|2|商品|
|3|个人中心|

```
second_jump
```
|code|含义|
| --------------  | :---: |
|11|维修项目主页|
|12|安装项目主页|
|21|商品主页|
|31|订单详情页|
|32|折扣券详情页|
|33|消息中心页|

```
third_jump
```
#####直接输入商品id或维修、安装id

##**注册**
#####注册流程
1、先向consumer/send_verify请求发送验证码验证手机
2、请求consumer/register注册成功或失败

#####顾客注册
######步骤一：
```
POST /consumer/send_verify
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
###**Request**
```
{"username":"18215606355","password":"123456","verify_code":"123456"}
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

##**消息**

#####获取消息中心未读消息数量
```
POST /consumer/get_unread_message_count
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
{
    "status": 1,
    "body": {
        "count": 1
    }
}
or
{"status": 13, "body": {"msg": "login first before other action"}}
```


##**消息**

#####设置消息为已读
```
POST /consumer/read_message
```
###**Parameters**
* username(_Required_|string)-用户名，必须为手机号
* private_token(_Required_|string)-用户token
* mid(_Required_|string)-消息id
###**Request**
```
{"username":"18215606355","private_token":"123456","mid":"1"}
```
###**Return**
```
{
    "status": 1,
    "body": {
        "msg": "message status change success"
    }
}
or
{
    "status": 7,
    "body": {
        "msg": "invalid mid"
    }
}
or
{"status": 13, "body": {"msg": "login first before other action"}}
```


##**反馈**

#####顾客提交反馈
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


##**商品**

#####获取一级商品列表
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

    "status": 1,
    "body": {
        "msg": "goods_p get success",
        "goods_item": [
            {
                "item_name": "冰箱维修",
                "have_advertisment": false,
                "pid": 2,
                "advertisment": ""
            },
            {
                "item_name": "水维修",
                "have_advertisment": false,
                "pid": 1,
                "advertisment": ""
            }
        ]
    }
}
or
{"status": 7, "body": {"msg": "invalid city number"}}
```

##**商品**

#####获取二级商品列表
```
POST /consumer/get_goods_sec_item
```
###**Parameters**
* pid(_Required_|string)-一级商品id
###**Request**
```
{"pid":"5"}
```
###**Return**
```
{
    "status": 1,
    "body": {
        "msg": "goods item_o get success",
        "goods": [
            {
                "item_name": "水管维修",
                "s_item_list": [
                    {
                        "picture": "",
                        "title": "屁股水管维修",
                        "sid": 1
                    },
                    {
                        "picture": "",
                        "title": "生育水管维修",
                        "sid": 2
                    }
                ],
                "oid": 1
            },
            {
                "item_name": "水龙头维修",
                "s_item_list": [
                    {
                        "picture": "",
                        "title": "小米水龙头",
                        "sid": 3
                    },
                    {
                        "picture": "",
                        "title": "魅族水龙头",
                        "sid": 4
                    }
                ],
                "oid": 2
            }
        ],
        "pid": 1
    }
}
or
{"status": 7, "body": {"msg": "invalid city number"}}
```


##**商品**

#####获取商品详细
```
POST /consumer/get_goods_detail
```
###**Parameters**
* sid(_Required_|string)-商品id
###**Request**
```
{"sid":"5"}
```
###**Return**
```
{
    "status": 1,
    "body": {
        "real_price": 10,
        "picture": "",
        "title": "屁股水管维修",
        "repair_price": 5,
        "made_by": "小屁股",
        "material": "屁股肉",
        "made_in": "中国",
        "content": "说明",
        "plus": "附加内容",
        "sid": 1,
        "msg": "goods detail get success",
        "origin_price": 12,
        "brand": "屁股"
    }
}
or
{"status": 7, "body": {"msg": "invalid id"}}
```

##**订单**

#####生成含商品支付订单
```
POST /consumer/create_pay_order
```
###**Parameters**
* username(_Required_|string)-用户名，必须为手机号
* private_token(_Required_|string)-token
* address(_Required_|string)-用户地址
* city_number(_Required_|string)-城市统一编码
* coupon_id(_Optional_|string)-优惠券id
* send_type(_Required_|integer)-送货类型
* use_coupon(_Required_|bool)-是否使用优惠券
* channel(_Required_|string)-支付渠道(详见ping＋＋文档)
* online_pay(_Required_|bool)-是否在线支付
* submit_price(_Required_|float)-提交总价
* goods_items(_Required_|array)-商品列表
* ###sid(_Required_|string)-商品id
* ###use_repair(_Required_|bool)-是否需要安装
* home_items(_Required_|string)-维修服务列表
* ###hid(_Required_|string)-服务id

###**Request**
```
{"username":"18215606355","send_type":1,"private_token":"JKGVDnCIH7Ec+OuWPvNeRQtT4dwjoB0U","coupon_id":"20102101","use_coupon":false,"channel":"alipay","address":"kb258","online_pay":true,"city_number":"511000","submit_price":"35.0","goods_items":[{"sid":"1","use_repair":true},{"sid":"2","use_repair":false}],"home_items":[{"hid":"1"}]}
```
###**Return**
```
{
    "status": 1,
    "body": {
        "msg": "server create order success, but not sure ping++ create success",
        "charge_detail": {
            "order_no": "201503250100000018",
            "extra": {},
            "app": "app_DibTK09SavX9mHmH",
            "livemode": false,
            "currency": "cny",
            "time_settle": null,
            "time_expire": 1427356166,
            "id": "ch_zrLmnHG4unjHCyHOmLf904m1",
            "subject": "生育水管维修等",
            "failure_msg": null,
            "channel": "alipay",
            "metadata": {},
            "body": "说明#内功#",
            "credential": {
                "alipay": {
                    "orderInfo": "_input_charset=\"utf-8\"&body=\"说明#内功#\"&it_b_pay=\"1440m\"&notify_url=\"https%3A%2F%2Fapi.pingxx.com%2Fnotify%2Fcharges%2Fch_zrLmnHG4unjHCyHOmLf904m1\"&out_trade_no=\"201503250100000018\"&partner=\"2008978902273687\"&payment_type=\"1\"&seller_id=\"2008978902273687\"&service=\"mobile.securitypay.pay\"&subject=\"生育水管维修等\"&total_fee=\"35\"&sign=\"ckR5dmJQMTg4YWJMdmIxQ3VUeUhTZUxH\"&sign_type=\"RSA\""
                },
                "object": "credential"
            },
            "client_ip": "10.211.55.2",
            "description": null,
            "amount_refunded": 0,
            "refunded": false,
            "object": "charge",
            "paid": false,
            "amount_settle": 0,
            "time_paid": null,
            "failure_code": null,
            "refunds": {
                "url": "/v1/charges/ch_zrLmnHG4unjHCyHOmLf904m1/refunds",
                "has_more": false,
                "object": "list",
                "data": []
            },
            "created": 1427269766,
            "transaction_no": null,
            "amount": 3500
        }
    }
}
or
{
    "status": 1,
    "body": {
        "msg": "create off-line order success"
    }
}
or
{
    "status": 20,
    "body": {
        "msg": "submit price wrong"
    }
}
or
{
    "status": 7,
    "body": {
        "msg": "invalid city_number"
    }
}
or
{
    "status": 21,
    "body": {
        "msg": "the coupon has used, over due or is not belong you"
    }
}
```


##**订单**

#####查询订单支付状态
```
POST /consumer/get_charge_status
```
###**Parameters**
* phone(_Required_|string)-用户手机号
* private_token(_Required_|string)-consumer token
* order_id(_Required_|string)-订单id

###**Request**
```
{"username":"18215606355","private_token":"LpOrR6BxMiAYUalZXQH1yIbKFEnGtkvS","order_id":"201503270100000001"}
```
###**Return**
```
{
    "status": 1,
    "body": {
        "msg": "order status get success",
        "order_id": "201503270100000001",
        "paid": true
    }
}
or
{
    "status": 7,
    "body": {
        "msg": "invalid order id"
    }
}
or
{
    "status": 13,
    "body": {
        "msg": "login first before other action"
    }
}
```



##**订单**

#####生成不含商品预约订单
```
POST /consumer/create_appointment
```
###**Parameters**
* phone(_Required_|string)-用户手机号
* private_token(_Required_|string)-consumer token or 用户token
* address(_Required_|string)-用户地址
* city_number(_Required_|string)-城市统一编码
* login(_Required_|bool)-是否登陆用户
* use_coupon(_Required_|bool)-是否使用优惠券
* coupon_id(_Optional_|string)-优惠券id
* home_items(_Required_|string)-维修服务列表
* ###hid(_Required_|string)-服务id

###**Request**
```
{"phone":"18215606355","private_token":"LpOrR6BxMiAYUalZXQH1yIbKFEnGtkvS","address":"test","city_number":"511100","login":true,"order_phone":"1234567","use_coupon":true,"coupon_id":"20150330300008","home_items":[{"hid":"1"}]}
```
###**Return**
```
{
    "status": 1,
    "body": {
        "new_id": "2011111111111111",
        "msg": "appointment create success"
    }
}
or
{
    "status": 9,
    "body": {
        "msg": "phone is not verified"
    }
}
or
{
    "status": 7,
    "body": {
        "msg": "invalid city_number"
    }
}
or
{
    "status": 7,
    "body": {
        "msg": "home item id:10invalid"
    }
}
```


##**订单**

#####预约订单上传图片
```
POST /consumer/upload_pircture
```
###**Parameters**
* phone(_Required_|string)-用户手机号
* private_token(_Required_|string)-consumer token or 用户token
* login(_Required_|bool)-是否登陆用户
* appointment_id(_Required_|bool)-预约单id
* picindex(_Required_|string)-上传图片编号
* file(_Required_|file)-上传的图片

###**Request**
```
formdata, not json
```
###**Return**
```
{
    "status": 1,
    "body": {
        "msg": "upload picture success"
    }
}
or
{
    "status": 9,
    "body": {
        "msg": "token is not correct"
    }
}
or
{
    "status": 9,
    "body": {
        "msg": "phone is not verified"
    }
}
or
{
    "status": 7,
    "body": {
        "msg": "invalid appointment id"
    }
}
```



##**订单**

#####评价订单
```
POST /consumer/appraise
```
###**Parameters**
* username(_Required_|string)-用户手机号
* private_token(_Required_|string)-用户token
* order_id(_Required_|string)-订单id
* rate(_Required_|integer)-星级
* rb1(_Required_|bool)-具体勾选评价1
* rb2(_Required_|bool)-具体勾选评价2
* rb3(_Required_|bool)-具体勾选评价3
* rb4(_Required_|bool)-具体勾选评价4
* rb5(_Required_|bool)-具体勾选评价5
* rb6(_Required_|bool)-具体勾选评价6

###**Request**
```
{"order_id":"201503270000000006","username":"18215606355","private_token":"LpOrR6BxMiAYUalZXQH1yIbKFEnGtkvS","rate":"4","rb1":true,"rb2":true,"rb3":true,"rb4":true,"rb5":false,"rb6":false,"comment":"test"}
```
###**Return**
```
{
    "status": 1,
    "body": {
        "msg": "appraise success"
    }
}
or
{
    "status": 6,
    "body": {
        "msg": "the order has appraised"
    }
}
or
{
    "status": 7,
    "body": {
        "msg": "invalid order id"
    }
}
or
{
    "status": 9,
    "body": {
        "msg": "the order has been canceled"
    }
}
```


##**订单**

#####撤销订单(status=1的订单才能使用)
```
POST /consumer/cancel_order
```
###**Parameters**
* username(_Required_|string)-用户手机号
* private_token(_Required_|string)-用户token
* order_id(_Required_|string)-订单id

###**Request**
```
{"username":"18215606355","private_token":"LpOrR6BxMiAYUalZXQH1yIbKFEnGtkvS","order_id":"201503300100000009"}
```
###**Return**
```
{
    "status": 1,
    "body": {
        "msg": "order cancel success"
    }
}
or
{
    "status": 3,
    "body": {
        "msg": "the order can not be canceled",
        "order_status": 5
    }
}
or
{
    "status": 7,
    "body": {
        "msg": "invalid order id"
    }
}
```



##**订单**

#####获取所有订单
```
POST /consumer/get_all_orders
```
###**Parameters**
* username(_Required_|string)-用户手机号
* private_token(_Required_|string)-用户token

###**Request**
```
{"username":"18215606355","private_token":"LpOrR6BxMiAYUalZXQH1yIbKFEnGtkvS"}

```
###**Return**
```
{
    "status": 1,
    "body": {
        "msg": "get order list success",
        "order_list": [
            {
                "status": 1,
                "refund": false,
                "order_id": "201503300100000001",
                "charge_id": "ch_j5y5e1yPKu105Wr9mTqjTyXH",
                "paid": false,
                "create_time": "2015-03-30 15:54:39.636990+08:00",
                "address": "kb258",
                "if_appraise": false,
                "order_phone": "18215606355",
                "goods_list": [
                    {
                        "real_price": 20,
                        "repair_price": 4,
                        "title": "生育水管维修",
                        "origin_price": 30,
                        "use_repair": false
                    },
                    {
                        "real_price": 10,
                        "repair_price": 5,
                        "title": "屁股水管维修",
                        "origin_price": 12,
                        "use_repair": true
                    }
                ],
                "send_type": 1,
                "online_pay": true,
                "name": "",
                "order_type": 1,
                "use_coupon": false,
                "amount": 35,
                "home_itmes": [
                    {
                        "item_name": " "
                    }
                ],
                "request_refund": false,
                "channel": "alipay"
            }
        ]
    }
}
or
{
    "status": 6,
    "body": {
        "msg": "the order has appraised"
    }
}
or
{
    "status": 7,
    "body": {
        "msg": "invalid order id"
    }
}
or
{
    "status": 9,
    "body": {
        "msg": "the order has been canceled"
    }
}
```


##**订单**
#####验证非注册用户预约手机号
1、先向consumer/send_verify请求发送验证码验证手机
2、请求consumer/verify_consumer 验证手机号并得到consumer token

#####请求验证码
######步骤一：
```
POST /consumer/send_verify
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
POST /consumer/verify_consumer
```
###**Parameters**
* username(_Required_|string)-用户名，必须为手机号
* verify_code(_Required_|string)-验证码
###**Request**
```
{"username":"18215606355","verify_code":"123456"}
```
###**Return**
```
{
    "status": 1,
    "body": {
        "msg": "verify success",
        "private_token": "AqMxVDKmpUN2lE+WCyzbZ8sJ7dkfQhXa"
    }
}
or
{
    "status": 13,
    "body": {
        "msg": "verify fail"
    }
}
```


##**维修／安装**

#####获取维修／安装项目
```
POST /consumer/get_homeitem
```
###**Parameters**
* city_number(_Required_|string)-城市统一编码
###**Request**
```
{"city_number":"511000"}
```
###**Return**
```
{
    "status": 1,
    "body": {
        "msg": "get home items success",
        "parent_item_list": [
            {
                "note": "",
                "sort_id": null,
                "item_name": "123",
                "type": 1,
                "recommand": 1,
                "pid": 1,
                "icon": ""
            }
        ]
    }
}
or
{
    "status": 7,
    "body": {
        "msg": "invalid city number"
    }
}
```


##**维修／安装**

#####获取维修／安装项目详细
```
POST /consumer/get_homeitem_detail
```
###**Parameters**
* pid(_Required_|string)-父维修／安装项目id
###**Request**
```
{"pid":"1"}
```
###**Return**
```
{
    "status": 1,
    "body": {
        "msg": "get homeitems success",
        "home_items": [
            {
                "item_name": " ",
                "sort_id": null,
                "hid": 1,
                "pic_url": null
            },
            {
                "item_name": "test",
                "sort_id": 12,
                "hid": 2,
                "pic_url": ""
            },
            {
                "item_name": "test2",
                "sort_id": null,
                "hid": 3,
                "pic_url": ""
            }
        ]
    }
}
or
{
    "status": 7,
    "body": {
        "msg": "invalid pid"
    }
}
```

##**维修／安装**

#####获取商品推荐列表
```
POST /consumer/get_recommand
```
###**Parameters**
* recommand_id(_Required_|string)-推荐商品pid
###**Request**
```
{"pid":"1"}
```
###**Return**
```
{
    "status": 1,
    "body": {
        "msg": "recommand list get success",
        "recommand_list": [
            {
                "real_price": 20,
                "picture": "",
                "recommand": 10,
                "title": "生育水管维修",
                "repair_price": 4,
                "sid": 2,
                "origin_price": 30
            },
            {
                "real_price": 20,
                "picture": "",
                "recommand": 3,
                "title": "小米水龙头",
                "repair_price": 4,
                "sid": 3,
                "origin_price": 40
            },
            {
                "real_price": 20,
                "picture": "",
                "recommand": 1,
                "title": "魅族水龙头",
                "repair_price": 4,
                "sid": 4,
                "origin_price": 40
            },
            {
                "real_price": 10,
                "picture": "",
                "recommand": 0,
                "title": "屁股水管维修",
                "repair_price": 5,
                "sid": 1,
                "origin_price": 12
            }
        ]
    }
}
or
{
    "status": 1,
    "body": {
        "msg": "no recommand list",
        "recommand_list": []
    }
}
or
{
    "status": 7,
    "body": {
        "msg": "invalid recommand id"
    }
}
```


##**广告**

#####获取广告
```
POST /consumer/get_advertisment
```
###**Parameters**
* city_number(_Required_|string)-城市统一编码
###**Request**
```
{"city_number":"1"}
```
###**Return**
```
{
    "status": 1,
    "body": {
        "advertisment_list": [
            {
                "fields": {
                    "content": "化霜定时器（100L内）",
                    "third_jump": null,
                    "title": "生育水管维修",
                    "photo": "",
                    "area": 2,
                    "is_new": true,
                    "second_jump": 2,
                    "create_time": "2015-03-28T08:08:38.837Z",
                    "type": 1,
                    "first_jump": 3
                },
                "model": "HomeApi.advertisement",
                "pk": 2
            },
            {
                "fields": {
                    "content": "化霜定时器（100L内）",
                    "third_jump": 1,
                    "title": "小米水龙头",
                    "photo": "",
                    "area": 2,
                    "is_new": true,
                    "second_jump": 12,
                    "create_time": "2015-03-28T08:08:05.681Z",
                    "type": 1,
                    "first_jump": 1
                },
                "model": "HomeApi.advertisement",
                "pk": 1
            }
        ],
        "msg": "advertisment list get success"
    }
}
or
{
    "status": 7,
    "body": {
        "msg": "invalid city number
    }
}
```


##**优惠券**

#####检查游戏小游戏是否可玩
```
POST /consumer/check_game
```
###**Parameters**
* username(_Required_|string)-用户手机号
* private_token(_Required_|string)-用户token
###**Request**
```
{"username":"18215606355","private_token":"LpOrR6BxMiAYUalZXQH1yIbKFEnGtkvS"}
```
###**Return**
```
{
    "status": 1,
    "body": {
        "msg": "game status get success",
        "have_game": true
    }
}
or
{
    "status": 13,
    "body": {
        "msg": "login befor other action"
    }
}
```


##**优惠券**

#####进行小游戏
```
POST /consumer/play_game
```
###**Parameters**
* username(_Required_|string)-用户手机号
* private_token(_Required_|string)-用户token
###**Request**
```
{"username":"18215606355","private_token":"LpOrR6BxMiAYUalZXQH1yIbKFEnGtkvS"}
```
###**Return**
```
{
    "status": 1,
    "body": {
        "msg": "get coupon success",
        "deadline": 1459229553,
        "value": 3,
        "cou_id": "20150330300001"
    }
}
or
{
    "status": 7,
    "body": {
        "msg": "coupon send over number"
    }
}
or
{
    "status": 7,
    "body": {
        "msg": "no game can play"
    }
}
```


##**优惠券**

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
{
    "status": 1,
    "body": {
        "msg": "invite code exchange success",
        "deadline": 1459229781,
        "value": 5,
        "cou_id": "20150330100002"
    }
}
or
{
    "status": 6,
    "body": {
        "msg": "you have exchanged this invite code"
    }
}
or
{"status": 7, "body": {"msg": "no invite code info"}}
or
{"status": 14, "body": {"msg": "you can not exchange your own invite code"}}
```


##**优惠券**

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
{
    "status": 1,
    "body": {
        "coupons": [
            {
                "owned_time": "2015-03-25 12:58:50+08:00",
                "create_time": "2015-03-25 13:56:26.867416+08:00",
                "cou_id": "20102101",
                "deadline": 1427270400,
                "type": 1,
                "value": 5,
                "if_use": true
            },
            {
                "owned_time": "2015-03-30 13:32:33.560285+08:00",
                "create_time": "2015-03-30 13:32:33.560626+08:00",
                "cou_id": "20150330300001",
                "deadline": 1459200753,
                "type": 3,
                "value": 3,
                "if_use": false
            },
            {
                "owned_time": "2015-03-30 13:32:47.135290+08:00",
                "create_time": "2015-03-30 13:32:47.135509+08:00",
                "cou_id": "20150330300002",
                "deadline": 1459200767,
                "type": 3,
                "value": 8,
                "if_use": false
            },
            {
                "owned_time": "2015-03-30 13:32:48.579905+08:00",
                "create_time": "2015-03-30 13:32:48.580116+08:00",
                "cou_id": "20150330300003",
                "deadline": 1459200768,
                "type": 3,
                "value": 8,
                "if_use": false
            },
            {
                "owned_time": "2015-03-30 13:32:49.874741+08:00",
                "create_time": "2015-03-30 13:32:49.874962+08:00",
                "cou_id": "20150330300004",
                "deadline": 1459200769,
                "type": 3,
                "value": 8,
                "if_use": false
            },
            {
                "owned_time": "2015-03-30 13:32:50.778640+08:00",
                "create_time": "2015-03-30 13:32:50.778853+08:00",
                "cou_id": "20150330300005",
                "deadline": 1459200770,
                "type": 3,
                "value": 1,
                "if_use": false
            },
            {
                "owned_time": "2015-03-30 13:32:51.665107+08:00",
                "create_time": "2015-03-30 13:32:51.665324+08:00",
                "cou_id": "20150330300006",
                "deadline": 1459200771,
                "type": 3,
                "value": 2,
                "if_use": false
            },
            {
                "owned_time": "2015-03-30 13:32:52.738587+08:00",
                "create_time": "2015-03-30 13:32:52.738792+08:00",
                "cou_id": "20150330300007",
                "deadline": 1459200772,
                "type": 3,
                "value": 9,
                "if_use": false
            },
            {
                "owned_time": "2015-03-30 13:32:53.882715+08:00",
                "create_time": "2015-03-30 13:32:53.882936+08:00",
                "cou_id": "20150330300008",
                "deadline": 1459200773,
                "type": 3,
                "value": 4,
                "if_use": false
            },
            {
                "owned_time": "2015-03-30 13:32:54.756321+08:00",
                "create_time": "2015-03-30 13:32:54.756538+08:00",
                "cou_id": "20150330300009",
                "deadline": 1459200774,
                "type": 3,
                "value": 9,
                "if_use": false
            },
            {
                "owned_time": "2015-03-30 13:36:21.236433+08:00",
                "create_time": "2015-03-30 13:36:21.236651+08:00",
                "cou_id": "20150330100002",
                "deadline": 1459200981,
                "type": 1,
                "value": 5,
                "if_use": false
            }
        ]
    }
}
or
{"status": 13, "body": {"msg": "login first before other action"}}
```