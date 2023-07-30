from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm

from .models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('member_id', )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('member_id', 'authority', 'name', 'age', 'gender',)


class CustomUserDeleteForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('is_active',)


class AdminLoginForm(forms.Form):
    member_id = forms.CharField(
        error_messages={
            'required': 'Please enter Admin. member ID'
        },
        max_length=4, label='member_id'
    )
    password = forms.CharField(
        error_messages={
            'required': 'Please enter password'
        },
        label='password', widget=forms.PasswordInput
    )

    def clean(self):
        cleaned_data = super().clean()
        member_id = cleaned_data.get('member_id')
        password = cleaned_data.get('password')

        if member_id and password:
            try:
                user = User.objects.get(member_id=member_id)
                if not user.is_admin:
                    self.add_error('member_id', 'You should enter Admin. member ID')
                if password != user.password:
                    self.add_error('password', 'You should enter correct password')
            except Exception:
                self.add_error('member_id', 'You\'ve entered invalid member ID')
