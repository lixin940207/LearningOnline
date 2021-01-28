from datetime import datetime

from django.db import models

from apps.organizations.models import Teacher
from apps.users.models import BaseModel

DIFFICULTY_CHOICE = (
    ("cj", "primary"),
    ("zj", "medium"),
    ("gj", "advanced")
)
class Course(BaseModel):
    tacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="course name", max_length=50)
    desc = models.CharField(verbose_name="course description", max_length=300)
    time_duration = models.IntegerField(default=0, verbose_name="course duration(minuites)")
    degree = models.CharField(verbose_name="difficulty", choices=DIFFICULTY_CHOICE, max_length=10)
    students = models.IntegerField(default=0, verbose_name="number of students")
    fav_num = models.IntegerField(default=0, verbose_name="number of collects")
    category = models.CharField(default="backend development", max_length=20, verbose_name="course category")
    tag = models.CharField(default="", verbose_name="course tags", max_length=20)
    youneed_know = models.CharField(default="", max_length=300, verbose_name="course notice")
    teacher_tell = models.CharField(default="", max_length=300, verbose_name="teacher's words")
    detail = models.TextField(verbose_name="course detail")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name="cover image", max_length=100)

    class Meta:
        verbose_name = "course"




class Lesson(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="lesson name")
    time_duration = models.IntegerField(default=0, verbose_name="learning duration")

    class Meta:
        verbose_name = "lesson"

class Video(BaseModel):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="video name")
    time_duration = models.IntegerField(default=0, verbose_name="time duration")
    url = models.CharField(max_length=200, verbose_name="access address")

    class Meta:
        verbose_name = "video"

class CourseResource(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="resource name")
    file = models.FileField(upload_to="course/resourses/%Y/%m", max_length=200)
