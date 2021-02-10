from django.core.paginator import PageNotAnInteger
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator

from apps.operations.models import UserFavorite
from apps.organizations.forms import AddConsultForm
from apps.organizations.models import CourseOrg, City, Teacher


class TeacherDetailView(View):
    def get(self, request, teacher_id, *args, **kwargs):
        teacher = Teacher.objects.get(id=int(teacher_id))

        is_favorite_teacher = False
        is_favorite_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.id, fav_type=3):
                is_favorite_teacher = True
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.org.id, fav_type=2):
                is_favorite_org = True

        hot_teachers = Teacher.objects.all().order_by("-click_nums")[:3]

        return render(request, "teacher-detail.html",
                      {
                          "teacher": teacher,
                          "is_favorite_teacher": is_favorite_teacher,
                          "is_favorite_org": is_favorite_org,
                          "hot_teachers": hot_teachers,
                      })

class TeacherView(View):
    def get(self, request, *args, **kwargs):
        all_teachers = Teacher.objects.all()

        for teacher in all_teachers:
            total_students = 0
            total_comments = 0
            for course in teacher.course_set.all():
                total_students += course.students
                total_comments += course.coursecomment_set.count()
            teacher.total_students = total_students
            teacher.total_comments = total_comments

        # search
        keywords = request.GET.get("keywords", "")
        s_type = "teacher"
        if keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=keywords))

        # sort
        sort = request.GET.get("sort", "")
        if sort == "hot":
            all_teachers = all_teachers.order_by("-click_nums")

        teacher_num = all_teachers.count()

        # hot teachers
        hot_teachers = all_teachers.order_by("-click_nums")[:3]

        # pagination
        try:
            page = request.GET.get("page", 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teachers, per_page=5, request=request)
        teachers = p.page(page)

        return render(request, "teachers-list.html",
                      {
                          "all_teachers": teachers,
                          "teacher_nums": teacher_num,
                          "sort": sort,
                          "hot_teachers": hot_teachers,
                          "keywords": keywords,
                          "s_type": s_type
                       })


class OrgDescView(View):
    def get(self, request, org_id, *args, **kwargs):
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        return render(request, "org-detail-desc.html",
                      {
                          "course_org": course_org,
                          "current_page": "desc",
                      })


class OrgCourseView(View):
    def get(self, request, org_id, *args, **kwargs):
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        is_favorite = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                is_favorite = True

        all_courses = course_org.course_set.all()

        # pagination
        try:
            page = request.GET.get("page", 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, per_page=5, request=request)
        courses = p.page(page)
        return render(request, "org-detail-course.html",
                      {
                          "all_courses": courses,
                          "course_org": course_org,
                          "current_page": "course",
                          "is_favorite": is_favorite,
                      })


class OrgTeacherView(View):
    def get(self, request, org_id, *args, **kwargs):
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        is_favorite = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                is_favorite = True

        all_teachers = course_org.teacher_set.all()

        for teacher in all_teachers:
            total_students = 0
            total_comments = 0
            for course in teacher.course_set.all():
                total_students += course.students
                total_comments += course.coursecomment_set.count()
            teacher.total_students = total_students
            teacher.total_comments = total_comments

        return render(request, "org-detail-teachers.html",
                      {
                          "all_teachers": all_teachers,
                          "course_org": course_org,
                          "current_page": "teacher",
                          "is_favorite": is_favorite,
                      })


class OrgHomeView(View):
    def get(self, request, org_id, *args, **kwargs):
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        is_favorite = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                is_favorite = True

        all_courses = course_org.course_set.all()[:4]
        all_teachers = course_org.teacher_set.all()[:3]

        for teacher in all_teachers:
            total_students = 0
            total_comments = 0
            for course in teacher.course_set.all():
                total_students += course.students
                total_comments += course.coursecomment_set.count()
            teacher.total_students = total_students
            teacher.total_comments = total_comments

        return render(request, "org-detail-homepage.html",
                      {
                          "all_courses": all_courses,
                          "all_teachers": all_teachers,
                          "course_org": course_org,
                          "current_page": "home",
                          "is_favorite": is_favorite,
                      })


class AddConsultView(View):
    def post(self, request, *args, **kwargs):
        userconsult_form = AddConsultForm(request.POST)
        if userconsult_form.is_valid():
            userconsult = userconsult_form.save(commit=True)
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "fail", "msg": "Consult fail."})


class OrgView(View):
    def get(self, request, *args, **kwargs):
        all_orgs = CourseOrg.objects.all()
        all_cities = City.objects.all()

        # hot orgs
        hot_orgs = all_orgs.order_by("-click_nums")[:3]

        # search
        keywords = request.GET.get("keywords", "")
        s_type = "org"
        if keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=keywords) | Q(desc__icontains=keywords))

        # filter category
        category = request.GET.get("ct", "")
        if category:
            all_orgs = all_orgs.filter(category=category)

        # filter city
        city_id = request.GET.get("city", "")
        if city_id and city_id.isdigit():
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # sort
        sort = request.GET.get("sort", "")
        if sort == "students":
            all_orgs = all_orgs.order_by("-students")
        elif sort == "courses":
            all_orgs = all_orgs.order_by("-course_nums")

        org_nums = all_orgs.count()

        # pagination
        try:
            page = request.GET.get("page", 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, per_page=8, request=request)
        orgs = p.page(page)

        return render(request, "org-list.html",
                      {
                          "all_orgs": orgs,
                          "org_nums": org_nums,
                          "all_cities": all_cities,
                          "category": category,
                          "city_id": city_id,
                          "sort": sort,
                          "hot_orgs": hot_orgs,
                          "keywords": keywords,
                          "s_type": s_type
                       })