from django import forms


class PostForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)
    topic = forms.IntegerField()
