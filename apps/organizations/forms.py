from django import forms

from apps.operations.models import UserConsult


class AddConsultForm(forms.ModelForm):
    class Meta:
        model = UserConsult
        fields = ["name", "mobile", "course_name"]