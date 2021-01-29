import xadmin

from apps.courses.models import Course, Lesson, Video, CourseResource


class GlobalSetting(object):
    site_title = "Authorization Manager"
    site_footer = "lixin"


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'time_duration', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'teacher__name', 'desc', 'detail', 'degree', 'time_duration', 'students']
    list_editable = ["degree", "desc"]


class LessonAdmin(object):
    list_display = ['course', 'name', 'created_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'created_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'created_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'created_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'file', 'created_time']
    search_fields = ['course', 'name', 'file']
    list_filter = ['course', 'name', 'file', 'created_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)

xadmin.site.register(xadmin.views.CommAdminView, GlobalSetting)
xadmin.site.register(xadmin.views.BaseAdminView, BaseSetting)