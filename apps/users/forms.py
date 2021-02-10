from django import forms

from apps.users.models import UserProfile


class ChangePwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)

    def clean(self):
        pwd1 = self.cleaned_data["password1"]
        pwd2 = self.cleaned_data["password2"]

        if pwd1 != pwd2:
            raise forms.ValidationError("密码不一致")
        return self.cleaned_data


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["nick_name", "birthday", "gender", "address"]


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["avatar"]



class RegisterPostForm(forms.Form):
    nick_name = forms.CharField(required=True, min_length=2, max_length=20)
    password = forms.CharField(required=True)

    def clean_username(self):
        nick_name = self.data.get("nick_name")
        # 验证手机号码是否已经注册
        users = UserProfile.objects.filter(nick_name=nick_name)
        if users:
            raise forms.ValidationError("username exists")
        return nick_name



class LoginForm(forms.Form):
    username = forms.CharField(required=True, min_length=2)
    password = forms.CharField(required=True, min_length=3)