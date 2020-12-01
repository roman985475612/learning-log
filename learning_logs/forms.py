from django import forms

from .models import Tag, Entry, Comment


class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ['title', 'color']
        labels = {
            'title': '',
            'color': '',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter tag name'
            }),
            'color': forms.Select(attrs={
                'class': 'form-control',
            })
        }


class EntryForm(forms.ModelForm):

    class Meta:
        model = Entry
        fields = [
            'tag',
            'title', 
            'text',
            'image',
        ]
        labels = {
            'title': 'Header',
            'text': 'Text',
            'image': 'Photo',
            'tag': 'Tags'
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',   
                'placeholder': 'Enter header'
            }),
            'text': forms.Textarea(attrs={
                'cols': 40,
                'class': 'form-control', 
                'placeholder': 'Enter text article'
            }),
            'tag': forms.SelectMultiple(attrs={
                'class': 'form-select',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            })
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text': 'Leave a Comment:'
        }

        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 5,
                'class': 'form-control',
                'placeholder': 'Enter your comment...'
            })
        }
