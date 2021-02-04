from datetime import datetime

from django.db import models

from apps.organizations.models import Teacher, CourseOrg
from apps.users.models import BaseModel

DIFFICULTY_CHOICE = (
    ("cj", "primary"),
    ("zj", "medium"),
    ("gj", "advanced")
)


class Course(BaseModel):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="Teacher")
    course_org = models.ForeignKey(CourseOrg, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Course Organization")
    name = models.CharField(verbose_name="Course Name", max_length=50)
    desc = models.CharField(verbose_name="Course Description", max_length=300)
    time_duration = models.IntegerField(default=0, verbose_name="Course Duration(minutes)")
    degree = models.CharField(verbose_name="Difficulty", choices=DIFFICULTY_CHOICE, max_length=10)
    students = models.IntegerField(default=0, verbose_name="Student Number")
    click_num = models.IntegerField(default=0, verbose_name="Number of Clicks")
    fav_num = models.IntegerField(default=0, verbose_name="Number of Collects")
    notice = models.CharField(default="", verbose_name="Course Notice", max_length=300)
    category = models.CharField(default="backend development", max_length=20, verbose_name="Course Category")
    # tag = models.CharField(default="", verbose_name="Course Tag", max_length=20)
    youneed_know = models.CharField(default="", max_length=300, verbose_name="You Need to Know")
    teacher_tell = models.CharField(default="", max_length=300, verbose_name="Teacher's Words")
    is_classical = models.BooleanField(default=False, verbose_name="if Top")
    detail = models.TextField(verbose_name="Course Detail")
    is_banner = models.BooleanField(default=False, verbose_name="if advertising")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name="Cover Image", max_length=100)

    def __str__(self):
        return self.name


class CourseTag(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Course")
    tag = models.CharField(max_length=100, verbose_name="Tag")

    def __str__(self):
        return self.tag


class Lesson(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="lesson name")
    time_duration = models.IntegerField(default=0, verbose_name="learning duration")

    def __str__(self):
        return self.name


class Video(BaseModel):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="video name")
    time_duration = models.IntegerField(default=0, verbose_name="time duration")
    url = models.CharField(max_length=1000, verbose_name="access address")

    def __str__(self):
        return self.name


class CourseResource(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="resource name")
    file = models.FileField(upload_to="course/resourses/%Y/%m", max_length=200)

    def __str__(self):
        return self.name
