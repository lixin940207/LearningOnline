from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger

from apps.courses.models import Course, CourseTag, CourseResource, Video
from apps.operations.models import UserFavorite, UserCourse, CourseComment


class CourseVideoView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, course_id, video_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))
        course.click_num += 1
        course.save()

        video = Video.objects.get(id=int(video_id))

        # resources for download
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            UserCourse.objects.create(user=request.user, course=course)
            course.students += 1
            course.save()
        course_resource = CourseResource.objects.filter(course=course)

        # 学习过这个课程的人也会学习
        all_users = [user.user_id for user in UserCourse.objects.filter(course=course)]
        recommended_courses = [user_course.course for user_course in
                               UserCourse.objects.filter(user__id__in=all_users).exclude(course=course).order_by(
                                   "-course__click_num")[:5]]
        recommended_courses = list(set(recommended_courses))

        return render(request, "course-play.html", {
            "course": course,
            "course_resource": course_resource,
            "recommended_courses": recommended_courses,
            "video": video,
        })


class CourseCommentView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, course_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))
        course.click_num += 1
        course.save()

        course_comments = CourseComment.objects.filter(course=course)

        # 学习过这个课程的人也会学习
        all_users = [user.user_id for user in UserCourse.objects.filter(course=course)]
        recommended_courses = [user_course.course for user_course in
                               UserCourse.objects.filter(user__id__in=all_users).exclude(course=course).order_by(
                                   "-course__click_num")[:5]]
        recommended_courses = list(set(recommended_courses))

        return render(request, "course-comment.html", {
            "course": course,
            "course_comments": course_comments,
            "recommended_courses": recommended_courses,
        })


class CourseLessonView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, course_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))
        course.click_num += 1
        course.save()

        # resources for download
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            UserCourse.objects.create(user=request.user, course=course)
            course.students += 1
            course.save()
        course_resource = CourseResource.objects.filter(course=course)

        # 学习过这个课程的人也会学习
        all_users = [user.user_id for user in UserCourse.objects.filter(course=course)]
        recommended_courses = [user_course.course for user_course in
                               UserCourse.objects.filter(user__id__in=all_users).exclude(course=course).order_by(
                                   "-course__click_num")[:5]]
        recommended_courses = list(set(recommended_courses))

        return render(request, "course-lesson.html", {
            "course": course,
            "course_resource": course_resource,
            "recommended_courses": recommended_courses,
        })


class CourseDetailView(View):
    def get(self, request, course_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))
        course.click_num += 1
        course.save()

        ## check if user favorited the course
        is_favorited_course = False
        is_favorited_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                is_favorited_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                is_favorited_org = True

        # recommend courses according to course tag
        tags = [tag.tag for tag in course.coursetag_set.all()]
        recommend_courses = [coursetag.course for coursetag in
                             CourseTag.objects.filter(tag__in=tags).exclude(course_id=course.id).distinct()]

        return render(request, "course-detail.html", {
            "course": course,
            "is_favorited_course": is_favorited_course,
            "is_favorited_org": is_favorited_org,
            "recommend_courses": recommend_courses,
        })


class CourseListView(View):
    def get(self, request, *args, **kwargs):
        all_courses = Course.objects.all()
        recommend_courses = all_courses.order_by("-click_num")[:3]

        # search
        s_type = "course"
        keywords = request.GET.get("keywords", "")
        if keywords:
            all_courses = all_courses.filter(Q(name__icontains=keywords)|Q(desc__icontains=keywords)|Q(detail__icontains=keywords))

        # sort
        sort = request.GET.get("sort", "")
        if not sort:
            all_courses = all_courses.order_by("-created_time")
        elif sort == "hot":
            all_courses = all_courses.order_by("-fav_num")
        elif sort == "students":
            all_courses = all_courses.order_by("-students")

        # pagination
        try:
            page = request.GET.get("page", 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, per_page=2, request=request)
        courses = p.page(page)

        return render(request, "course-list.html", {
            "all_courses": courses,
            "sort": sort,
            "recommend_courses": recommend_courses,
            "keywords": keywords,
            "s_type": s_type,
        })
