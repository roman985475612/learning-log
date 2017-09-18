from django.contrib import admin

from .models import Topic, Tag, Entry, Comment


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'date_added', 'owner',)
    list_filter = ('date_added', 'owner',)
    search_fields = ['title']
    date_hierarchy = 'date_added'
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):

    def shorted_text(self, obj):
        return obj.text_short()

    shorted_text.short_description = "Text"

    list_display = ('title', 'views', 'shorted_text', 'owner', 'topic', 'date_added',)
    list_display_links = ('title', 'shorted_text',)
    list_filter = ('topic', 'date_added', 'owner',)
    search_fields = ['title', 'text']
    date_hierarchy = 'date_added'
    prepopulated_fields = {'slug': ('title',)}

    inlines = [CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'entry', 'date_added', 'owner')
    list_filter = ('entry', 'owner', 'date_added')
    search_fields = ['text']
    date_heerarchy = 'date_added'
