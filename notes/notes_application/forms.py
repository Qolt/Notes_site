from django import forms

class NoteForm(forms.Form):
    title = forms.CharField(required=False)
    text = forms.CharField(widget=forms.HiddenInput(), required=False)
    OPTIONS = (
                    ('', 'Priority'),
                    (u'Low', 'Low'),
                    (u'Normal', 'Normal'),
                    (u'High', 'High'),
                    (u'Very High', 'Very High'),
                )
    importance = forms.ChoiceField(widget=forms.Select, choices=OPTIONS, required=False)
