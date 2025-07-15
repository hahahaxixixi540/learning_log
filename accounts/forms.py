from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    """扩展默认的用户创建表单，添加额外字段"""
    email = forms.EmailField(required=True)
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}), 
        required=False,
        label='个人简介'
    )
    location = forms.CharField(
        max_length=100, 
        required=False,
        label='所在地'
    )
    birth_date = forms.DateField(
        required=False,
        label='出生日期'
    )
    
    class Meta:
        model = User
        fields = (
            'username', 
            'email', 
            'password1', 
            'password2',
            'bio',
            'location',
            'birth_date'
        )
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    """个人资料表单"""
    class Meta:
        model = Profile
        fields = [
            'profile_pic', 
            'bio', 
            'location', 
            'birth_date'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': '介绍一下你自己...'}),
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'profile_pic': '头像',
            'bio': '个人简介',
            'location': '所在地',
            'birth_date': '出生日期',
        }