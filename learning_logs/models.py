from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class Topic(models.Model):
    """用户学习笔记中的主题（支持公开分享）"""
    text = models.CharField(
        _("主题名称"),
        max_length=200,
        help_text=_("主题名称最大长度为200个字符")
    )
    date_added = models.DateTimeField(
        _("创建时间"),
        auto_now_add=True,
        db_index=True
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("所属用户"),
        related_name="topics"
    )
    is_public = models.BooleanField(
        _("是否公开"),
        default=False,
        help_text=_("勾选后该主题可通过链接分享给他人")
    )
    share_password = models.CharField(
        _("访问密码"),
        max_length=50,
        blank=True,
        null=True,
        help_text=_("可选：设置访问密码，为空则无需密码")
    )
    share_expire_at = models.DateTimeField(
        _("过期时间"),
        blank=True,
        null=True,
        help_text=_("可选：设置分享过期时间，为空则永久有效")
    )
    
    def __str__(self):
        return self.text
    
    def save(self, *args, **kwargs):
        if self.share_expire_at and self.share_expire_at < timezone.now():
            self.is_public = False
        if not self.is_public:
            self.share_password = None
            self.share_expire_at = None
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = _("主题")
        verbose_name_plural = _("主题")
        ordering = ["-date_added"]

class Entry(models.Model):
    """与主题相关的具体条目内容（新增音频支持）"""
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        verbose_name=_("关联主题"),
        related_name="entries"
    )
    text = models.TextField(_("条目内容"))
    # 图片字段
    image = models.ImageField(
        _("条目图片"),
        upload_to="entry_media/images/%Y/%m/%d/",
        blank=True,
        null=True
    )
    # 视频字段
    video = models.FileField(
        _("条目视频"),
        upload_to="entry_media/videos/%Y/%m/%d/",
        blank=True,
        null=True
    )
    # 音频字段
    audio = models.FileField(
        _("条目音频"),
        upload_to="entry_media/audio/%Y/%m/%d/",
        blank=True,
        null=True,
        help_text=_("可选：上传音频文件（支持MP3、WAV格式）")
    )
    date_added = models.DateTimeField(_("创建时间"), auto_now_add=True)
    
    @property
    def like_count(self):
        return self.likes.count()
    
    def __str__(self):
        return f"{self.text[:50]}..."
    
    class Meta:
        verbose_name = _("条目")
        verbose_name_plural = _("条目")
        ordering = ["-date_added"]

class Like(models.Model):
    """点赞模型"""
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entry_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('entry', 'user')  # 防止重复点赞

class Comment(models.Model):
    """评论模型（支持嵌套回复）"""
    entry = models.ForeignKey(
        Entry,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='entry_comments'
    )
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    
    class Meta:
        ordering = ['created_at']
    
    def is_parent(self):
        return self.parent is None
    
    def get_replies(self):
        return self.replies.all()

# 新增：条目收藏模型（完全独立，不影响现有模型）
class EntryBookmark(models.Model):
    """用户收藏条目模型"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookmarked_entries',  # 反向关联：user.bookmarked_entries.all()
        verbose_name=_("收藏用户")
    )
    entry = models.ForeignKey(
        Entry,
        on_delete=models.CASCADE,
        related_name='bookmarked_by',  # 反向关联：entry.bookmarked_by.all()
        verbose_name=_("被收藏条目")
    )
    bookmarked_at = models.DateTimeField(
        _("收藏时间"),
        auto_now_add=True,
        db_index=True
    )
    
    class Meta:
        unique_together = ('user', 'entry')  # 同一用户不能重复收藏同一条目
        ordering = ['-bookmarked_at']  # 按收藏时间倒序
        verbose_name = _("条目收藏")
        verbose_name_plural = _("条目收藏")
    
    def __str__(self):
        return f"{self.user.username} 收藏了 {self.entry.text[:20]}"