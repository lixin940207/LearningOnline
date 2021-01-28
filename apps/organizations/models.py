from django.db import models

from apps.users.models import BaseModel

ORGANIZATION_CATEGORY_CHOICES = (
    ("pxjg", "training institution"),
    ("gr", "person"),
    ("gx", "university")
)

class City(BaseModel):
    name = models.CharField(max_length=200, verbose_name="city name")

class CourseOrg(BaseModel):
    name = models.CharField(max_length=50, verbose_name="organization name")
    desc = models.TextField(verbose_name="description")
    tag = models.CharField(default="famous", max_length=20, verbose_name="organization tag")
    category = models.CharField(default="pxjg", verbose_name="organization category", max_length=10,
                                choices=ORGANIZATION_CATEGORY_CHOICES)
    click_nums = models.IntegerField(default=0, verbose_name="number of hits")
    fav_nums = models.IntegerField(default=0, verbose_name="number of collects")
    image = models.ImageField(max_length=100, upload_to="org/%Y/%m", verbose_name="logo")
    address = models.CharField(max_length=150, verbose_name="organization address")
    students = models.IntegerField(default=0, verbose_name="number of students")
    course_nums = models.IntegerField(default=0, verbose_name="number of courses")
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="city")

class Teacher(BaseModel):
    #user = models.OneToOneField(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="用户")
    org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name="organization")
    name = models.CharField(max_length=50, verbose_name="teacher name")
    work_years = models.IntegerField(default=0, verbose_name="working years")
    work_company = models.CharField(max_length=50, verbose_name="working company")
    work_position = models.CharField(max_length=50, verbose_name="working position")
    points = models.CharField(max_length=50, verbose_name="teaching specialties")
    click_nums = models.IntegerField(default=0, verbose_name="number of hits")
    fav_nums = models.IntegerField(default=0, verbose_name="number of collects")
    age = models.IntegerField(default=18, verbose_name="age")
    image = models.ImageField(upload_to="teacher/%Y/%m", verbose_name="avatar", max_length=100)