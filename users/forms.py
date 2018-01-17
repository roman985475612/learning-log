from django import forms

from .models import Person


class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        exclude = ('owner',)
        labels = {
            'first_name': 'First name:',
            'last_name': 'Last name:',
            'sex': 'Genger',
            'birth_date': 'Birth date',
            'email': 'E-mail',
            'home_page': 'Home page',
            'about_me': 'About me',
            'image': 'Photo'
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'required',
                'placeholder': 'Enter your first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'required',
                'placeholder': 'Enter your last name'
            }),
            'sex': forms.Select(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
            'birth_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Enter your birthdate'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your e-mail'
            }),
            'home_page': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your home page URL'
            }),
            'about_me': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tell us about yourself...'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }
