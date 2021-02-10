from django.conf.urls import url
from django.urls import path

from apps.organizations.views import OrgView, AddConsultView, OrgHomeView, OrgTeacherView, OrgCourseView, OrgDescView, \
    TeacherView, TeacherDetailView

urlpatterns = [
    url(r'^list/$', OrgView.as_view(), name="list"),
    url(r'^add_consult/', AddConsultView.as_view(), name="add_consult"),
    path('<int:org_id>/', OrgHomeView.as_view(), name="home"),
    path('<int:org_id>/teacher/', OrgTeacherView.as_view(), name="teacher"),
    path('<int:org_id>/course/', OrgCourseView.as_view(), name="course"),
    path('<int:org_id>/desc/', OrgDescView.as_view(), name="desc"),
    path('teachers/', TeacherView.as_view(), name="teacher-list"),
    path('teacher_list/<int:teacher_id>/', TeacherDetailView.as_view(), name="teacher-detail"),

]