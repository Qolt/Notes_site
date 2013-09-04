from django import forms

class NoteForm(forms.Form):
    title = forms.CharField(required=False)
    text = forms.CharField(widget=forms.Textarea, required=False)
