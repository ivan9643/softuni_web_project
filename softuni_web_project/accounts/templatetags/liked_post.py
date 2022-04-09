from django import template

register = template.Library()


@register.filter(name='liked_by')
def post_liked_by(value, user_id):
    users_liked_ids = [user.id for user in value.likes.all()]
    return user_id in users_liked_ids
