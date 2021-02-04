from django import forms

from apps.operations.models import UserFavorite, CourseComment


class UserFavForm(forms.ModelForm):
    class Meta:
        model = UserFavorite
        fields = ["fav_id", "fav_type"]


class CourseCommentForm(forms.ModelForm):
    class Meta:
        model = CourseComment
        fields = ["course", "comment"]