from django import forms

from .models import Tag, Entry, Comment


class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ['title', 'color']


class EntryForm(forms.ModelForm):

    class Meta:
        model = Entry
        fields = ['image', 'tag', 'title', 'text']
        labels = {'image': '', 'tag': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 40})}


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'rows': 5})}
