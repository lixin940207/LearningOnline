from django.db import models
from django.contrib.auth import get_user_model
from apps.courses.models import Course
from apps.users.models import BaseModel

UserProfile = get_user_model()


class UserConsult(BaseModel):
    name = models.CharField(max_length=20)
    mobile = models.CharField(max_length=11)
    course_name = models.CharField(max_length=50)


class CourseComment(BaseModel):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)


class UserFavorite(BaseModel): # 目前有三种类型的用户收藏，不需要建三张表，而且方便扩展
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    fav_id = models.IntegerField(verbose_name="数据id")
    fav_type = models.IntegerField(choices=((1,"course"),(2,"organization"),(3,"teacher")), default=1, verbose_name="favorite type")


class UserMessage(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    message = models.CharField(max_length=200, verbose_name="message content")
    has_read = models.BooleanField(default=False, verbose_name="if read")


class UserCourse(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)