from django.db import models
from django.contrib.auth import get_user_model
from apps.courses.models import Course
from apps.users.models import BaseModel

UserProfile = get_user_model()


class UserConsult(BaseModel):
    name = models.CharField(max_length=20)
    mobile = models.CharField(max_length=11)
    course_name = models.CharField(max_length=50)

    def __str__(self):
        return "{name}_{course}({mobile})".format(name=self.name, course=self.course_name, mobile=self.mobile)


class CourseComment(BaseModel):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)

    def __str__(self):
        return self.comment


class UserFavorite(BaseModel): # 目前有三种类型的用户收藏，不需要建三张表，而且方便扩展
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    fav_id = models.IntegerField(verbose_name="数据id")
    fav_type = models.IntegerField(choices=((1,"course"),(2,"organization"),(3,"teacher")), default=1, verbose_name="favorite type")

    def __str__(self):
        return "{user}_{id}".format(user=self.user.username, id=self.fav_id)


class UserMessage(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    message = models.CharField(max_length=200, verbose_name="message content")
    has_read = models.BooleanField(default=False, verbose_name="if read")

    def __str__(self):
        return self.message


class UserCourse(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.course.name