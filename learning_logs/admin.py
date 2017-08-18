from django.contrib import admin

from .models import Topic, Entry


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'date_added',)
    list_filter = ('date_added',)
    search_fields = ['title']
    date_hierarchy = 'date_added'
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):

    def shorted_text(self, obj):
        return obj.text_short()

    shorted_text.short_description = "Text"

    list_display = ('title', 'slug', 'shorted_text', 'topic', 'date_added',)
    list_display_links = ('title', 'slug', 'shorted_text',)
    list_filter = ('topic', 'date_added',)
    search_fields = ['title', 'text']
    date_hierarchy = 'date_added'
    prepopulated_fields = {'slug': ('title',)}
