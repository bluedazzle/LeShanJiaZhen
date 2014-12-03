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

class HomeAdmin(AbstractBaseUser):
    username = models.CharField(max_length=50)
    log_time = models.DateTimeField(max_length=20)
    reg_time = models.DateTimeField(auto_now_add=True)
    type = models.IntegerField(max_length=2, default=1)
    verify = models.BooleanField(default=False)
    work_num = models.CharField(max_length=50, null=True, blank=True)
    area = models.CharField(max_length=20)


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

    def __unicode__(self):
        return self.phone

class Appointment(models.Model):
    content = models.CharField(max_length=500)
    create_time = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(max_length=2)
    photo = models.CharField(max_length=100, blank=True, null=True)
    process_by = models.ForeignKey(HomeAdmin, blank=True, null=True)
    consumer = models.ForeignKey(Consumer)

    def __unicode__(self):
        return self.content

class HomeItem_P(models.Model):
    item_name = models.CharField(max_length=10)
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.item_name

class HomeItem_O(models.Model):
    item_name = models.CharField(max_length=50)
    create_time = models.DateTimeField(auto_now_add=True)
    parent_item = models.ForeignKey(HomeItem_P)

    def __unicode__(self):
        return self.item_name

class HomeItem(models.Model):
    title = models.CharField(max_length=30)
    content = models.CharField(max_length=500)
    create_time = models.DateTimeField(auto_now_add=True)
    parent_item = models.ForeignKey(HomeItem_O, null=True, blank=True)

    def __unicode__(self):
        return self.title

class Advertisement(models.Model):
    content = models.CharField(max_length=500, blank=True, null=True)
    photo = models.CharField(max_length=50, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    is_new = models.BooleanField(default=True)

    def __unicode__(self):
        return unicode(self.create_time)

class Block(models.Model):
    area_name = models.CharField(max_length=10)
    area_tel = models.IntegerField(max_length=20)
    area_info = models.CharField(max_length=1000, null=True, blank=True)
    area_admin = models.ForeignKey(HomeAdmin, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)

    def __unicode__(self):
        return self.area_name

class Notice(models.Model):
    content = models.CharField(max_length=100)
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.content

class PhoneVerify(models.Model):
    phone = models.IntegerField(max_length=20)
    verify = models.IntegerField(max_length=10)
    update_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.phone



