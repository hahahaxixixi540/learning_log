from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import ProfileForm, CustomUserCreationForm
from .models import Profile

def register(request):
    """处理用户注册"""
    if request.method != 'POST':
        form = CustomUserCreationForm()
    else:
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            
            # 移除手动创建Profile的代码，让信号处理器负责
            # Profile.objects.create(...)
            
            login(request, new_user)
            return redirect('accounts:profile')
    
    context = {'form': form}
    return render(request, 'registration/register.html', context)

@login_required
def profile(request):
    """显示和编辑用户个人资料"""
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=profile)
    
    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def profile_edit(request):
    """用户编辑个人资料视图"""
    profile = request.user.profile
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=profile)
    
    context = {'form': form}
    return render(request, 'accounts/profile_edit.html', context)

@login_required
def view_other_profile(request, username):
    """查看其他用户的个人资料"""
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    
    context = {
        'viewed_user': user,
        'profile': profile,
    }
    return render(request, 'accounts/other_profile.html', context)

def custom_login(request):
    """自定义登录视图"""
    if request.user.is_authenticated:
        return redirect('learning_logs:index')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('accounts:profile')
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})

def custom_logout(request):
    """自定义登出视图"""
    logout(request)
    return redirect('learning_logs:index')