from django import template
register = template.Library()

@register.inclusion_tag('learning_logs/comments_tree.html')
def render_comments(comments, reply_to=None, user=None, topic=None):
  
    return {
        'comments': comments,
        'reply_to': reply_to,
        'user': user,
        'topic': topic  
    }