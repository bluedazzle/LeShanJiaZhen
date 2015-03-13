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
    phone = models.CharField(max_length=15)
    verified = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=100, null=True)

    def __unicode__(self):
        return self.phone

class Appointment(models.Model):
    content = models.CharField(max_length=500)
    create_time = models.DateTimeField(auto_now_add=True)
    appointment_id = models.CharField(max_length=100, null=True)
    remark = models.CharField(max_length=100, blank=True, null=True)
    status = models.IntegerField(max_length=2)
    photo1 = models.CharField(max_length=100, blank=True, null=True)
    photo2 = models.CharField(max_length=100, blank=True, null=True)
    photo3 = models.CharField(max_length=100, blank=True, null=True)
    photo4 = models.CharField(max_length=100, blank=True, null=True)
    appoint_time = models.DateTimeField(blank=True, null=True)
    address = models.CharField(max_length=100, default='')
    name = models.CharField(max_length=10, default='')
    area = models.ForeignKey(Block)
    process_by = models.ForeignKey(HomeAdmin, blank=True, null=True)
    consumer = models.ForeignKey(Consumer)
    service_person = models.CharField(max_length=20, blank=True, null=True)
    service_time = models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return self.content

class HomeItem_P(models.Model):
    item_name = models.CharField(max_length=10)
    type = models.IntegerField(max_length=2)
    create_time = models.DateTimeField(auto_now_add=True)
    area = models.ForeignKey(Block, null=True, blank=True)
    icon = models.CharField(max_length=100, blank=True, null=True)
    sort_id = models.IntegerField(max_length=10, blank=True, null=True)

    def __unicode__(self):
        return self.item_name

class HomeItem_O(models.Model):
    item_name = models.CharField(max_length=50)
    create_time = models.DateTimeField(auto_now_add=True)
    parent_item = models.ForeignKey(HomeItem_P)
    sort_id = models.IntegerField(max_length=10, blank=True, null=True)

    def __unicode__(self):
        return self.item_name

class HomeItem(models.Model):
    title = models.CharField(max_length=30)
    price = models.CharField(max_length=10, blank=True, null=True)
    content = models.CharField(max_length=500)
    create_time = models.DateTimeField(auto_now_add=True)
    parent_item = models.ForeignKey(HomeItem_P, null=True, blank=True)
    sort_id = models.IntegerField(max_length=20, blank=True, null=True)

    def __unicode__(self):
        return self.title


class Advertisement(models.Model):
    content = models.CharField(max_length=500, blank=True, null=True)
    photo = models.CharField(max_length=150, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    is_new = models.BooleanField(default=True)

    def __unicode__(self):
        return unicode(self.create_time)




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
    sex = models.IntegerField(max_length=1, null=True, blank=True)
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
    cou_id = models.CharField(max_length=14, unique=True)
    value = models.IntegerField(max_length=3)
    if_use = models.BooleanField(default=False)
    type = models.IntegerField(max_length=2)
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
    game_sign = models.CharField(max_length=6, null=True, blank=True)
    game_active = models.BooleanField(default=False)

    online_money_low = models.FloatField(max_length=5, null=True, blank=True)
    online_money_high = models.FloatField(max_length=5, null=True, blank=True)
    online_active = models.BooleanField(default=False)

    reg_money = models.FloatField(max_length=5, null=True, blank=True)

    invite_money = models.FloatField(max_length=5, null=True, blank=True)

    def __unicode__(self):
        return self.id

class Message(models.Model):
    content = models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(max_length=30, null=True, blank=True)
    own = models.ForeignKey(Associator, related_name='messages')

    def __unicode__(self):
        return self.content

class Goods_P(models.Model):
    item_name = models.CharField(max_length=30)
    create_time = models.DateTimeField(auto_now_add=True)
    area = models.ForeignKey(Block, related_name='goodsp')
    sort_id = models.IntegerField(max_length=10, blank=True, null=True)
    advertisement = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.item_name

class Goods_O(models.Model):
    item_name = models.CharField(max_length=50)
    create_time = models.DateTimeField(auto_now_add=True)
    parent_item = models.ForeignKey(Goods_P, related_name='goodso')
    sort_id = models.IntegerField(max_length=10, blank=True, null=True)
    goods_advertisment = models.CharField(max_length=100, null=True, blank=True)
    have_advertisment = models.BooleanField(default=False)

    def __unicode__(self):
        return self.item_name

class GoodsItem(models.Model):
    title = models.CharField(max_length=40)
    brand = models.CharField(max_length=15, null=True, blank=True)
    material = models.CharField(max_length=15, null=True, blank=True)
    made_by = models.CharField(max_length=15, null=True, blank=True)
    made_in = models.CharField(max_length=20, null=True, blank=True)
    content = models.CharField(max_length=100, null=True, blank=True)
    origin_price = models.FloatField(max_length=10, null=True, blank=True)
    real_price = models.FloatField(max_length=10)
    repair_price = models.FloatField(max_length=10, null=True, blank=True)
    picture = models.CharField(max_length=100, null=True, blank=True)
    recommand = models.IntegerField(max_length=10, null=True, blank=True, default=0)
    parent_item = models.ForeignKey(Goods_O, related_name='goodsitems')

    def __unicode__(self):
        return self.title

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

class AppControl(models.Model):
    android_version = models.CharField(max_length=10, null=True, blank=True)
    ios_version = models.CharField(max_length=10, null=True, blank=True)
    android_update_time = models.DateTimeField(max_length=30, null=True, blank=True)
    ios_update_time = models.DateTimeField(max_length=30, null=True, blank=True)

    def __unicode__(self):
        return str(self.id)

