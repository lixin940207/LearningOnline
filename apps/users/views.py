from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger

from apps.courses.models import Course
from apps.operations.models import UserFavorite, UserMessage, Banner, UserProfile
from apps.organizations.models import CourseOrg, Teacher
from apps.users.forms import LoginForm, UploadImageForm, UserInfoForm, ChangePwdForm, RegisterPostForm


def message_nums(request):
    """
    Add media-related context variables to the context.
    """
    if request.user.is_authenticated:
        return {'unread_nums': request.user.usermessage_set.filter(has_read=False).count()}
    else:
        return {}


class MyMessageView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        messages = UserMessage.objects.filter(user=request.user)
        current_page = "message"
        for message in messages:
            message.has_read = True
            message.save()

        # 对讲师数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(messages, per_page=5, request=request)
        messages = p.page(page)

        return render(request, "usercenter-message.html",{
            "messages":messages,
            "current_page":current_page
        })


class MyFavCourseView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "myfav_course"
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            try:
                course = Course.objects.get(id=fav_course.fav_id)
                course_list.append(course)
            except Course.DoesNotExist as e:
                pass
        return render(request, "usercenter-fav-course.html",{
            "course_list":course_list,
            "current_page":current_page
        })

class MyFavTeacherView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "myfav_teacher"
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            org = Teacher.objects.get(id=fav_teacher.fav_id)
            teacher_list.append(org)
        return render(request, "usercenter-fav-teacher.html",{
            "teacher_list":teacher_list,
            "current_page":current_page
        })


class MyFavOrgView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "myfav_org"
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org = CourseOrg.objects.get(id=fav_org.fav_id)
            org_list.append(org)
        return render(request, "usercenter-fav-org.html",{
            "org_list":org_list,
            "current_page":current_page
        })


class MyCourseView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        # my_courses = UserCourse.objects.filter(user=request.user)
        return render(request, "usercenter-mycourse.html",{
            # "my_courses":my_courses,
            "current_page": "mycourse"
        })


class ChangePwdView(LoginRequiredMixin, View):
    login_url = "/login/"
    def post(self, request, *args, **kwargs):
        pwd_form = ChangePwdForm(request.POST)
        if pwd_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            user = request.user
            user.set_password(pwd1)
            user.save()
            # login(request, user)

            return JsonResponse({
                "status":"success"
            })
        else:
            return JsonResponse(pwd_form.errors)


class UploadImageView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return JsonResponse({
                "status": "success",
            })
        else:
            return JsonResponse({
                "status": "fail",
            })


class UserInfoView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        return render(request, "usercenter-info.html", {
            "current_page": "info"
        })

    def post(self, request, *args, **kwargs):
        userinfo_form = UserInfoForm(request.POST, instance=request.user)
        if userinfo_form.is_valid():
            userinfo_form.save()
            return JsonResponse({
                "status": "success",
            })
        else:
            return JsonResponse(userinfo_form.errors)


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        banners = Banner.objects.all()[:3]
        return render(request, "register.html", {
            "banners": banners,
        })

    def post(self, request, *args, **kwargs):
        register_post_form = RegisterPostForm(request.POST)
        if register_post_form.is_valid():
            nick_name = register_post_form.cleaned_data["nick_name"]
            password = register_post_form.cleaned_data["password"]
            # 新建一个用户
            user = UserProfile(username=nick_name, nick_name=nick_name)
            user.set_password(password)
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "register.html", {
                "register_post_form": register_post_form
            })


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        banners = Banner.objects.all()[:3]
        next = request.GET.get("next", "")
        return render(request, "login.html", {
            "next": next,
            "banners": banners,
        })

    def post(self, request, *args, **kwargs):
        # form validation
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            # 使用django提供的内置方法来判断用户名和密码是否存在
            user = authenticate(username=user_name, password=password)
            if user is not None:
                # check if user can login
                login(request, user)
                # return render(request, "index.html")
                next = request.GET.get("next", "")
                if next:
                    return HttpResponseRedirect(next)
                else:
                    return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "login.html", {
                    "msg": "Username or password incorrect.",
                    "login_form": login_form
                })
        else:
            return render(request, "login.html", {"login_form": login_form})