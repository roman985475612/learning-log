from django.contrib import admin

from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('text', 'date_added',)
    list_filter = ['date_added']
    date_hierarchy = 'date_added'
    search_fields = ['text']


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'votes',)
    list_filter = ['question__text']
    search_fields = ['text']
