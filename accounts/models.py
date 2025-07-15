from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

class Profile(models.Model):
    """用户个人资料模型"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to='profile_pics/', 
        default='profile_pics/default.png',
        verbose_name='头像'
    )
    bio = models.TextField(
        max_length=500, 
        blank=True,
        verbose_name='个人简介'
    )
    location = models.CharField(
        max_length=100, 
        blank=True,
        verbose_name='所在地'
    )
    birth_date = models.DateField(
        null=True, 
        blank=True,
        verbose_name='出生日期'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user.username} 的个人资料'
    
    class Meta:
        verbose_name = '个人资料'
        verbose_name_plural = '个人资料'

# 信号处理器
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic():
            Profile.objects.create(user=instance)
