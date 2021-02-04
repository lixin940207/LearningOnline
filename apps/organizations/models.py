from django.db import models

from apps.users.models import BaseModel

ORGANIZATION_CATEGORY_CHOICES = (
    ("pxjg", "Training Institution"),
    ("gr", "Individual"),
    ("gx", "University")
)


class City(BaseModel):
    name = models.CharField(max_length=200, verbose_name="City Name", null=False)

    def __str__(self):
        return self.name


class CourseOrg(BaseModel):
    name = models.CharField(max_length=50, verbose_name="Organization Name")
    desc = models.TextField(verbose_name="Description")
    tag = models.CharField(default="famous", max_length=20, verbose_name="Organization Tag")
    category = models.CharField(default="pxjg", verbose_name="Organization Category", max_length=10,
                                choices=ORGANIZATION_CATEGORY_CHOICES)
    click_nums = models.IntegerField(default=0, verbose_name="Number of Hits")
    fav_nums = models.IntegerField(default=0, verbose_name="Number of Collects")
    image = models.ImageField(max_length=100, upload_to="org/%Y/%m", verbose_name="Logo")
    address = models.CharField(max_length=150, verbose_name="Organization Address")
    students = models.IntegerField(default=0, verbose_name="Number of Students")
    course_nums = models.IntegerField(default=0, verbose_name="Number of Courses")
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="City")
    is_auth = models.BooleanField(default=False, verbose_name="if authenticated")
    is_golden = models.BooleanField(default=False, verbose_name="if golden")

    def get_top_courses(self):
        return self.course_set.filter(is_classical=True)[:3]

    def __str__(self):
        return self.name


class Teacher(BaseModel):
    #user = models.OneToOneField(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="用户")
    org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name="Organization")
    name = models.CharField(max_length=50, verbose_name="Teacher Name")
    work_years = models.IntegerField(default=0, verbose_name="Work Years")
    work_company = models.CharField(max_length=50, verbose_name="Work Company")
    work_position = models.CharField(max_length=50, verbose_name="Work Position")
    points = models.CharField(max_length=50, verbose_name="Teaching Specialties")
    click_nums = models.IntegerField(default=0, verbose_name="Number of Hits")
    fav_nums = models.IntegerField(default=0, verbose_name="Number of Collects")
    age = models.IntegerField(default=18, verbose_name="Age")
    image = models.ImageField(upload_to="teacher/%Y/%m", verbose_name="Avatar", max_length=100)

    def __str__(self):
        return self.name