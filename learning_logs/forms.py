from django import forms

from .models import Topic, Tag, Entry, Comment


class TopicForm(forms.ModelForm):

    class Meta:
        model = Topic
        fields = ['title']
        labels = {'title': ''}


class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ['title', 'color']


class EntryForm(forms.ModelForm):

    class Meta:
        model = Entry
        fields = ['image', 'tag', 'title', 'text']
        labels = {'image': '', 'tag': '', 'title': '', 'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 40})}


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'rows': 5})}
