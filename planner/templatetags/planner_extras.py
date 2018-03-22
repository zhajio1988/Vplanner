from django import template
from planner.models import Project
from django.template import Context

register = template.Library()

@register.inclusion_tag('planner/cats.html')
def get_category_list(cat=None):
    return {'cats':Project.objects.all(), 'act_cat': cat}

@register.simple_tag
def get_verbose_field_name(instance, field_name):
    """
    Returns verbose_name for a field.
    """
    return instance._meta.get_field(field_name).verbose_name.title()

@register.inclusion_tag('planner/submit_line.html', takes_context=True)
def submit_row(context):
    """
    Displays the row of buttons for delete and save.
    """
    show_save = context.get('show_save', True)
    show_save_and_continue = context.get('show_save_and_continue', True)
    ctx = Context(context)
    ctx.update({
        'show_delete_link': True,
        'show_save_and_add_another': True,
        'show_save_and_continue': show_save_and_continue,
        'show_save': show_save,
    })
    return ctx

#{% load verbose_names %}
#{% get_verbose_field_name test_instance "name" %}
