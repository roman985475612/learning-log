from django import forms

from .models import Choice


class VoteForm(forms.Form):

    vote = forms.ModelChoiceField(
        queryset=None,
        empty_label=None,
        widget=forms.RadioSelect(),
    )

    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question')
        super(VoteForm, self).__init__(*args, **kwargs)
        self.fields['vote'].queryset = Choice.objects.filter(question=self.question)
