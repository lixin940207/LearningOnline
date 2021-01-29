from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

GENDER_CHOICES = (
    ("male", "男"),
    ("female", "女")
)

class BaseModel(models.Model):
    created_time = models.DateTimeField(default=datetime.now, verbose_name="created time")
    class Meta:
        abstract=True

class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name="nickname", default="")
    birthday = models.DateField(verbose_name="birthday", null=True, blank=True)
    gender = models.CharField(verbose_name="sex", choices=GENDER_CHOICES, max_length=6)
    address = models.CharField(max_length=200, verbose_name="address", default="")
    mobile = models.CharField(max_length=11, verbose_name="phone number") # 默认手机号注册
    avatar = models.ImageField(upload_to="head_image/%Y/%m", default="head_image/default.jpg")

    def __str__(self):
        return self.nick_name
