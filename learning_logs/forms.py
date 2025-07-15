from django import forms
from .models import Topic, Entry, Comment

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        # 新增audio字段
        fields = ['text', 'image', 'video', 'audio']
        labels = {
            'text': '',
            'image': '上传图片（可选）',
            'video': '上传视频（可选）',
            'audio': '上传音频（可选）'  # 音频字段标签
        }
        widgets = {
            'text': forms.Textarea(attrs={'cols': 80, 'rows': 6}),
        }

class CommentForm(forms.ModelForm):
    """支持无JS回复的评论表单"""
    parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False, initial=0)
    show_reply = forms.BooleanField(widget=forms.HiddenInput, required=False, initial=False)
    
    class Meta:
        model = Comment
        fields = ['text', 'parent_id', 'show_reply']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': '添加评论...',
                'class': 'form-control'
            }),
        }
        labels = {'text': ''}