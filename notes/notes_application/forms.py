from django import forms

class NoteForm(forms.Form):
    title = forms.CharField(required=False)
    text = forms.CharField(widget=forms.HiddenInput(), required=False)
    OPTIONS = (
                    ('0', 'Priority'),
                    ('1', 'Low'),
                    ('2', 'Normal'),
                    ('3', 'High'),
                    ('4', 'Very High'),
                )
    importance = forms.ChoiceField(widget=forms.Select, choices=OPTIONS, required=False)
