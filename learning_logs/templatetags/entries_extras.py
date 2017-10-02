from django import template

from learning_logs.models import Entry

register = template.Library()


@register.simple_tag
def get_three_popular_entries():

    return Entry.objects.order_by('-likes')[:3]
