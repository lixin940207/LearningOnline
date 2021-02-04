from django.conf.urls import url

from apps.operations.views import AddFavView, AddCommentView

urlpatterns = [
    url(r'fav/$', AddFavView.as_view(), name="fav"),
    url(r'comment/$', AddCommentView.as_view(), name="comment"),

]