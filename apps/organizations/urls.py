from django.conf.urls import url
from django.urls import path

from apps.organizations.views import OrgView, AddConsultView, OrgHomeView, OrgTeacherView, OrgCourseView, OrgDescView, \
    TeacherView, TeacherDetailView

urlpatterns = [
    url(r'^list/$', OrgView.as_view(), name="list"),
    url(r'^add_consult/', AddConsultView.as_view(), name="add_consult"),
    url(r'^(?P<org_id>\d)/$', OrgHomeView.as_view(), name="home"),
    url(r'^(?P<org_id>\d)/teacher/$', OrgTeacherView.as_view(), name="teacher"),
    url(r'^(?P<org_id>\d)/course/$', OrgCourseView.as_view(), name="course"),
    url(r'^(?P<org_id>\d)/desc/$', OrgDescView.as_view(), name="desc"),
    url(r'^teachers/$', TeacherView.as_view(), name="teacher-list"),
    url(r'^teacher_list/(?P<teacher_id>\d)/$', TeacherDetailView.as_view(), name="teacher-detail"),

]