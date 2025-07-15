from django import template
register = template.Library()

@register.inclusion_tag('learning_logs/comments_tree.html')
def render_comments(comments, reply_to=None, user=None, topic=None):
    """
    渲染评论树的自定义标签
    新增topic参数，支持模板中传递主题信息
    """
    return {
        'comments': comments,
        'reply_to': reply_to,
        'user': user,
        'topic': topic  # 新增：接收主题参数
    }