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
        fields = ['text', 'image', 'video']
        labels = {
            'text': '',
            'image': '上传图片（可选）',
            'video': '上传视频（可选）'
        }
        widgets = {
            'text': forms.Textarea(attrs={'cols': 80, 'rows': 6}),
        }

class CommentForm(forms.ModelForm):
    """支持无JS回复的评论表单"""
    # 父评论ID（标识回复对象）
    parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False, initial=0)
    # 控制回复表单显示的标记
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