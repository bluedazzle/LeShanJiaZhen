# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import hashlib
# Create your models here.


class HomeAdminManager(BaseUserManager):
    def create_user(self, email, phone, passwd=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email = HomeAdminManager.normalize_email(email),
            username = phone,
        )

        user.set_password(passwd)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, passwd):

        user = self.create_user(email,
            username = phone,
            password = passwd,
        )
        user.is_staff = True
        user.is_active = True
        user.is_admin = False
        user.save(using=self._db)
        return user

class AssociatorManager(BaseUserManager):
    def create_user(self, email, phone, passwd=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email = AssociatorManager.normalize_email(email),
            username = phone,
        )

        user.set_password(passwd)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, passwd):

        user = self.create_user(email,
            username = phone,
            password = passwd,
        )
        user.is_staff = True
        user.is_active = True
        user.is_admin = False
        user.save(using=self._db)
        return user


class Block(models.Model):
    city_num = models.CharField(max_length=10, unique=True)
    area_name = models.CharField(max_length=10)
    area_tel = models.CharField(max_length=20)
    area_address = models.CharField(max_length=100, null=True)
    area_info = models.CharField(max_length=1000, null=True, blank=True)
    # area_admin = models.ForeignKey(HomeAdmin, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.area_name


class HomeAdmin(AbstractBaseUser):
    username = models.CharField(max_length=50)
    nick = models.CharField(max_length=50, default='')
    log_time = models.DateTimeField(max_length=20)
    reg_time = models.DateTimeField(auto_now_add=True)
    type = models.IntegerField(max_length=2, default=1)
    verify = models.BooleanField(default=False)
    manage_game = models.BooleanField(default=False)
    manage_check_vip = models.BooleanField(default=False)
    manage_coupon = models.BooleanField(default=False)
    manage_send_message = models.BooleanField(default=False)
    work_num = models.CharField(max_length=50, null=True, blank=True)
    area = models.ForeignKey(Block, null=True, blank=True)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['username']
    objects = HomeAdminManager()

    def __unicode__(self):
        return self.username

    def is_authenticated(self):
        return True

    def hashed_password(self, password=None):
        if not password:
            return self.password
        else:
            return hashlib.md5(password).hexdigest()

    def check_password(self, password):
        if self.hashed_password(password) == self.password:
            return True
        return False

    class Meta:
        app_label = 'HomeApi'

class Consumer(models.Model):
    phone = models.CharField(max_length=15, unique=True)
    verified = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.phone



# class HomeItem(models.Model):
#     title = models.CharField(max_length=30)
#     price = models.CharField(max_length=10, blank=True, null=True)
#     content = models.CharField(max_length=500)
#     create_time = models.DateTimeField(auto_now_add=True)
#     parent_item = models.ForeignKey(HomeItem_P, null=True, blank=True)
#     sort_id = models.IntegerField(max_length=20, blank=True, null=True)
#
#     def __unicode__(self):
#         return self.title


class Advertisement(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=500, blank=True, null=True)
    photo = models.CharField(max_length=150, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    area = models.ForeignKey(Block)
    is_new = models.BooleanField(default=True)
    type = models.IntegerField(max_length=2, null=True, blank=True)
    first_jump = models.IntegerField(max_length=3, null=True, blank=True)
    second_jump = models.IntegerField(max_length=3, null=True, blank=True)
    third_jump = models.IntegerField(max_length=3, null=True, blank=True)

    def __unicode__(self):
        return unicode(self.title)




class Notice(models.Model):
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.content


class PhoneVerify(models.Model):
    phone = models.CharField(max_length=11)
    verify = models.IntegerField(max_length=10)
    update_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.phone


class Application(models.Model):
    old_area_id = models.IntegerField()
    new_area_id = models.IntegerField()
    apply_user = models.ForeignKey(HomeAdmin)
    apply_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return unicode(self.id)

class Associator(AbstractBaseUser):
    username = models.CharField(max_length=15, unique=True)
    # 1男2女默认3
    sex = models.IntegerField(max_length=1, default=3)
    birthday = models.DateTimeField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    invite_code = models.CharField(max_length=6, null=True, blank=True)
    device_code = models.CharField(max_length=128, null=True, blank=True)
    private_token = models.CharField(max_length=32, null=True, blank=True)
    reg_time = models.DateTimeField(auto_now_add=True)
    invite_str = models.CharField(max_length=1000, null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['username']
    objects = HomeAdminManager()

    def __unicode__(self):
        return self.username

    def is_authenticated(self):
        return True

    def hashed_password(self, password=None):
        if not password:
            return self.password
        else:
            return hashlib.md5(password).hexdigest()

    def check_password(self, password):
        if self.hashed_password(password) == self.password:
            return True
        return False

    class Meta:
        app_label = 'HomeApi'

class Coupon(models.Model):
    cou_id = models.CharField(max_length=15, unique=True)
    value = models.IntegerField(max_length=3)
    if_use = models.BooleanField(default=False)
    # 1为好友邀请，2为在线支付，3为游戏获取，4为注册，5为系统赠送
    type = models.IntegerField(max_length=2)
    # 游戏标识
    game_sign = models.CharField(max_length=6, null=True, blank=True)
    own = models.ForeignKey(Associator, null=True, blank=True, related_name='coupons')
    create_time = models.DateTimeField(auto_now=True)
    owned_time = models.DateTimeField(max_length=30, null=True, blank=True)
    deadline = models.DateTimeField(max_length=30)

    def __unicode__(self):
        return self.cou_id

class CouponControl(models.Model):
    game_money_low = models.FloatField(max_length=5, null=True, blank=True)
    game_money_high = models.FloatField(max_length=5, null=True, blank=True)
    game_start_time = models.DateTimeField(max_length=30, null=True, blank=True)
    game_end_time = models.DateTimeField(max_length=30, null=True, blank=True)
    game_coupon_num = models.IntegerField(max_length=10, null=True, blank=True)
    game_current_num = models.IntegerField(max_length=10, null=True, blank=True)
    game_sign = models.CharField(max_length=6, null=True, blank=True)
    game_active = models.BooleanField(default=False)

    online_money_low = models.IntegerField(max_length=5, null=True, blank=True)
    online_money_high = models.IntegerField(max_length=5, null=True, blank=True)
    online_active = models.BooleanField(default=False)

    reg_money = models.IntegerField(max_length=5, default=0)

    invite_money = models.IntegerField(max_length=5, default=0)

    def __unicode__(self):
        return str(self.id)


class GameRecord(models.Model):
    game_id = models.CharField(max_length=20)
    start_time = models.DateTimeField(max_length=30)
    end_time = models.DateTimeField(max_length=30, null=True, blank=True)
    money_high = models.FloatField(max_length=5)
    money_low = models.FloatField(max_length=5)
    origin_coupon_num = models.IntegerField(max_length=10)
    actually_coupon_num = models.IntegerField(max_length=10, default=0)
    game_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.game_id

class Message(models.Model):
    content = models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(max_length=30, null=True, blank=True)
    read = models.BooleanField(default=False)
    own = models.ForeignKey(Associator, related_name='messages')

    def __unicode__(self):
        return self.content

class Goods_P(models.Model):
    item_name = models.CharField(max_length=30)
    create_time = models.DateTimeField(auto_now_add=True)
    area = models.ForeignKey(Block, related_name='goodsp')
    sort_id = models.IntegerField(max_length=10, blank=True, null=True)
    advertisement = models.CharField(max_length=100, null=True, blank=True)
    have_advertisment = models.BooleanField(default=False)

    def __unicode__(self):
        return self.item_name

class Goods_O(models.Model):
    item_name = models.CharField(max_length=50)
    create_time = models.DateTimeField(auto_now_add=True)
    parent_item = models.ForeignKey(Goods_P, related_name='goodso')
    sort_id = models.IntegerField(max_length=10, blank=True, null=True)

    def __unicode__(self):
        return self.item_name

class GoodsItem(models.Model):
    title = models.CharField(max_length=40)
    brand = models.CharField(max_length=15, null=True, blank=True)
    sort_id = models.IntegerField(max_length=10, blank=True, null=True)
    material = models.CharField(max_length=15, null=True, blank=True)
    made_by = models.CharField(max_length=15, null=True, blank=True)
    made_in = models.CharField(max_length=20, null=True, blank=True)
    content = models.CharField(max_length=100, null=True, blank=True)
    plus = models.CharField(max_length=200, null=True, blank=True)
    origin_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    real_price = models.DecimalField(max_digits=10, decimal_places=2)
    repair_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    picture = models.CharField(max_length=100, null=True, blank=True)
    selled = models.IntegerField(max_length=10, default=0)
    #推荐权重
    recommand = models.IntegerField(max_length=10, null=True, blank=True, default=0)
    parent_item = models.ForeignKey(Goods_O, related_name='goodsitems')

    def __unicode__(self):
        return self.title


class HomeItem_P(models.Model):
    item_name = models.CharField(max_length=10)
    note = models.CharField(max_length=100, null=True, blank=True)
    type = models.IntegerField(max_length=2)
    create_time = models.DateTimeField(auto_now_add=True)
    area = models.ForeignKey(Block, null=True, blank=True)
    icon = models.CharField(max_length=100, blank=True, null=True)
    recommand = models.ForeignKey(Goods_P, blank=True, null=True, related_name='homeitem')
    sort_id = models.IntegerField(max_length=10, blank=True, null=True)

    def __unicode__(self):
        return self.item_name


class HomeItem(models.Model):
    item_name = models.CharField(max_length=50)
    create_time = models.DateTimeField(auto_now_add=True)
    parent_item = models.ForeignKey(HomeItem_P)
    sort_id = models.IntegerField(max_length=10, blank=True, null=True)
    pic_url = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.item_name


class Feedback(models.Model):
    phone = models.CharField(max_length=15)
    content = models.CharField(max_length=500)
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.phone

class Verify(models.Model):
    phone = models.CharField(max_length=15)
    verify = models.CharField(max_length=10)
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.phone

class AppControl(models.Model):
    android_version = models.CharField(max_length=10, null=True, blank=True)
    ios_version = models.CharField(max_length=10, null=True, blank=True)
    android_update_time = models.DateTimeField(max_length=30, null=True, blank=True)
    ios_update_time = models.DateTimeField(max_length=30, null=True, blank=True)

    def __unicode__(self):
        return str(self.id)


class Appointment(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    order_phone = models.CharField(max_length=15, default='000')
    order_id = models.CharField(max_length=100, unique=True)
    remark = models.CharField(max_length=100, blank=True, null=True)
    status = models.IntegerField(max_length=2)
    photo1 = models.CharField(max_length=100, blank=True, null=True)
    photo2 = models.CharField(max_length=100, blank=True, null=True)
    photo3 = models.CharField(max_length=100, blank=True, null=True)
    photo4 = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, default='')
    name = models.CharField(max_length=10, default='')
    area = models.ForeignKey(Block)
    process_by = models.ForeignKey(HomeAdmin, blank=True, null=True)
    consumer = models.ForeignKey(Consumer, null=True, blank=True)
    associator = models.ForeignKey(Associator, null=True, blank=True)
    service_person = models.CharField(max_length=20, default="无")
    service_time = models.CharField(max_length=50, default="无")
    # order_type = 1:goods, order_type = 2:homeitem
    order_type = models.IntegerField(max_length=4)
    online_pay = models.BooleanField(default=True)
    send_type = models.IntegerField(max_length=2, default=1)
    amount = models.FloatField(max_length=10, null=True, blank=True)
    valid = models.BooleanField(default=True)
    use_coupon = models.BooleanField(default=False)
    order_coupon = models.ForeignKey(Coupon, null=True, blank=True)

    if_appraise = models.BooleanField(default=False)
    comment = models.CharField(max_length=200, null=True, blank=True)
    rate = models.IntegerField(max_length=2, null=True, blank=True)
    # 上门及时
    rb1 = models.BooleanField(default=False)
    # 认真仔细
    rb2 = models.BooleanField(default=False)
    # 技术专业
    rb3 = models.BooleanField(default=False)
    # 收费公道
    rb4 = models.BooleanField(default=False)
    # 维修快速
    rb5 = models.BooleanField(default=False)
    # 态度良好
    rb6 = models.BooleanField(default=False)

    def __unicode__(self):
        return self.order_id




class OrderGoods(models.Model):
    title = models.CharField(max_length=40)
    brand = models.CharField(max_length=15, null=True, blank=True)
    material = models.CharField(max_length=15, null=True, blank=True)
    made_by = models.CharField(max_length=15, null=True, blank=True)
    made_in = models.CharField(max_length=20, null=True, blank=True)
    content = models.CharField(max_length=100, null=True, blank=True)
    plus = models.CharField(max_length=200, null=True, blank=True)
    origin_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    real_price = models.DecimalField(max_digits=10, decimal_places=2)
    repair_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    use_repair = models.BooleanField(default=True)
    picture = models.CharField(max_length=100, null=True, blank=True)
    #推荐权重
    origin_item = models.ForeignKey(GoodsItem, related_name='actgoods')
    belong = models.ForeignKey(Appointment, related_name='ordergoods')

    def __unicode__(self):
        return self.title



class OrderHomeItem(models.Model):
    item_name = models.CharField(max_length=50)
    create_time = models.DateTimeField(auto_now_add=True)
    origin_item = models.ForeignKey(HomeItem, related_name='actitem')
    belong = models.ForeignKey(Appointment, related_name='orderitem')

    def __unicode__(self):
        return self.item_name



class OnlineCharge(models.Model):
    pingpp_charge_id = models.CharField(max_length=64)
    order_id = models.CharField(max_length=20, unique=True)
    channel_id = models.CharField(max_length=64, null=True, blank=True)
    channel = models.CharField(max_length=20, default='miss')
    paid = models.BooleanField(default=False)
    refund_url = models.CharField(max_length=200, null=True, blank=True)
    request_refund = models.BooleanField(default=False)
    refund = models.BooleanField(default=False)
    refund_desc = models.CharField(max_length=300, null=True, blank=True)
    refund_fail_mes = models.CharField(max_length=300, null=True, blank=True)
    refund_id = models.CharField(max_length=64, null=True, blank=True)
    price = models.IntegerField(max_length=10)
    time_expire = models.DateTimeField(max_length=30, null=True, blank=True)
    pingpp_create_time = models.DateTimeField(max_length=30)
    create_time = models.DateTimeField(auto_now_add=True)
    order_with = models.OneToOneField(Appointment, related_name='chargeinfo')
    own = models.ForeignKey(Associator, related_name='charges')

    def __unicode__(self):
        return self.order_id
