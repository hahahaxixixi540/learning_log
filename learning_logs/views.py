from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseBadRequest
from django.db.models import Q
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from .models import Topic, Entry, Like, Comment
from .forms import TopicForm, EntryForm, CommentForm

def index(request):
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    return render(request, 'learning_logs/topics.html', {'topics': topics})

def topic(request, topic_id):
    """修复：通过会话记录密码验证状态，避免重复验证"""
    topic = get_object_or_404(Topic, id=topic_id)
    is_owner = (topic.owner == request.user)
    session_key = f"topic_{topic_id}_authenticated"  # 会话键：标记该主题已验证
    
    # 权限校验：优先判断是否为所有者
    if not is_owner:
        # 非所有者必须访问公开主题
        if not topic.is_public:
            raise Http404("该主题未公开或已被删除")
        # 检查是否过期
        if topic.share_expire_at and topic.share_expire_at < timezone.now():
            return HttpResponseBadRequest("该分享链接已过期")
        # 检查密码（通过会话记录验证状态，避免重复验证）
        if topic.share_password:
            # 已通过会话验证：直接放行
            if request.session.get(session_key, False):
                pass
            # 未验证：检查URL参数中的密码
            else:
                input_password = request.GET.get('password')
                if not input_password or input_password != topic.share_password:
                    return render(request, 'learning_logs/public_topic_password.html', {'topic': topic})
                # 验证通过：记录会话状态
                request.session[session_key] = True
    
    # 解析回复参数
    reply_to = request.GET.get('reply_to')
    try:
        reply_to = int(reply_to) if reply_to else None
    except ValueError:
        reply_to = None
    
    # 处理搜索和评论数据（保持原有逻辑）
    search_query = request.GET.get('q', '')
    entries = topic.entries.all().order_by('-date_added')
    for entry in entries:
        entry.user_liked = entry.likes.filter(user=request.user).exists() if request.user.is_authenticated else False
        entry.comment_count = entry.comments.count()
        entry.top_level_comments = entry.comments.filter(parent__isnull=True)
    
    if search_query:
        entries = entries.filter(Q(text__icontains=search_query))
    
    return render(request, 'learning_logs/topic.html', {
        'topic': topic,
        'entries': entries,
        'comment_form': CommentForm(),
        'search_query': search_query,
        'reply_to': reply_to,
        'is_owner': is_owner,  # 新增：传递是否为所有者的标记
    })

@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')
    return render(request, 'learning_logs/new_topic.html', {'form': form})

@login_required
def new_entry(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(request.POST, request.FILES)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)
    return render(request, 'learning_logs/new_entry.html', {'topic': topic, 'form': form})

@login_required
def edit_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    if entry.topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=entry.topic.id)
    return render(request, 'learning_logs/edit_entry.html', {'entry': entry, 'topic': entry.topic, 'form': form})

@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    if entry.topic.owner != request.user:
        raise Http404
    if request.method == 'POST':
        entry.delete()
        return redirect('learning_logs:topic', topic_id=entry.topic.id)
    return render(request, 'learning_logs/confirm_delete_entry.html', {'entry': entry, 'topic': entry.topic})

@login_required
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if topic.owner != request.user:
        raise Http404
    if request.method == 'POST':
        topic.delete()
        return redirect('learning_logs:topics')
    return render(request, 'learning_logs/confirm_delete_topic.html', {'topic': topic})

@login_required
def toggle_public_topic(request, topic_id):
    """完善公开状态切换逻辑"""
    topic = get_object_or_404(Topic, id=topic_id)
    if topic.owner != request.user:
        raise Http404
    
    if request.method == 'POST':
        topic.is_public = not topic.is_public
        topic.share_password = request.POST.get('share_password', '').strip() or None
        expire_str = request.POST.get('share_expire_at')
        if expire_str:
            naive_datetime = parse_datetime(expire_str)
            if naive_datetime:
                topic.share_expire_at = timezone.make_aware(naive_datetime)
            else:
                topic.share_expire_at = None
        else:
            topic.share_expire_at = None
        topic.save()
        return redirect('learning_logs:topic', topic_id=topic_id)
    
    context = {
        'topic': topic,
        'share_link': request.build_absolute_uri(f'/topics/{topic.id}/')
    }
    return render(request, 'learning_logs/toggle_public.html', context)

@login_required
def like_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    like, created = Like.objects.get_or_create(entry=entry, user=request.user)
    if not created:
        like.delete()
    # 点赞后重定向，保留密码参数（若有）
    redirect_url = request.META.get('HTTP_REFERER', f'/topics/{entry.topic.id}/')
    return redirect(redirect_url)

@login_required
def add_comment(request, entry_id):
    """修复：允许已验证的非所有者提交评论"""
    entry = get_object_or_404(Entry, id=entry_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            parent_id = form.cleaned_data.get('parent_id')
            comment = form.save(commit=False)
            comment.entry = entry
            comment.user = request.user  # 只需登录即可评论，无需是所有者
            
            if parent_id and parent_id != 0:
                try:
                    parent_comment = Comment.objects.get(id=parent_id, entry=entry)
                    comment.parent = parent_comment
                except Comment.DoesNotExist:
                    pass
            
            comment.save()
    # 评论后重定向，保留密码参数（若有）
    redirect_url = request.META.get('HTTP_REFERER', f'/topics/{entry.topic.id}/')
    return redirect(redirect_url)