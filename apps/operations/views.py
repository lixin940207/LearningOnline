from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.base import View

from apps.courses.models import Course
from apps.operations.forms import UserFavForm, CourseCommentForm
from apps.operations.models import UserFavorite, CourseComment, Banner
from apps.organizations.models import CourseOrg, Teacher


class IndexView(View):
    def get(self, request, *args, **kwargs):
        banners = Banner.objects.all().order_by("index")
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, "index.html", {
            "banners": banners,
            "courses": courses,
            "banner_courses": banner_courses,
            "course_orgs": course_orgs
        })


class AddCommentView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": "fail",
                "msg": "user not logged in."
            })
        comment_form = CourseCommentForm(request.POST)
        if comment_form.is_valid():
            course = comment_form.cleaned_data["course"]
            comment = comment_form.cleaned_data["comment"]

            CourseComment.objects.create(user=request.user, course=course, comment=comment)
            return JsonResponse({
                "status": "success",
            })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "parameter error."
            })

class AddFavView(View):
    def post(self, request, *args, **kwargs):
        # check if user logged in
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": "fail",
                "msg": "user not logged in."
            })
        userfav_form = UserFavForm(request.POST)
        if userfav_form.is_valid():
            fav_id = userfav_form.cleaned_data["fav_id"]
            fav_type = userfav_form.cleaned_data["fav_type"]

            # check if already favorite
            existed_records = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
            if existed_records:
                existed_records.delete()
                if fav_type == 1:
                    course = Course.objects.get(id=fav_id)
                    course.fav_num -= 1
                    course.save()
                elif fav_type == 2:
                    org = CourseOrg.objects.get(id=fav_id)
                    org.fav_nums -= 1
                    org.save()
                else:
                    teacher = Teacher.objects.get(id=fav_id)
                    teacher.fav_nums -= 1
                    teacher.save()
                return JsonResponse({
                    "status": "success",
                    "msg": "Favorite"
                })
            else:
                userfav = UserFavorite.objects.create(user=request.user, fav_id=fav_id, fav_type=fav_type)
                if fav_type == 1:
                    course = Course.objects.get(id=fav_id)
                    course.fav_num += 1
                    course.save()
                elif fav_type == 2:
                    org = CourseOrg.objects.get(id=fav_id)
                    org.fav_nums += 1
                    org.save()
                else:
                    teacher = Teacher.objects.get(id=fav_id)
                    teacher.fav_nums += 1
                    teacher.save()
                return JsonResponse({
                    "status": "success",
                    "msg": "Favorited"
                })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "parameter error."
            })