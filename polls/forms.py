from django import forms

from .models import Choice


class VoteForm(forms.Form):
	def __init__(self, *args, **kwargs):
		self.question = kwargs.pop('question')
		return super(VoteForm, self).__init__(*args, **kwargs)

	vote = forms.ModelChoiceField(
		queryset=Choice.objects.get(question=self.question),
		empty_label=None,
		widget=forms.RadioSelect(),
	)
