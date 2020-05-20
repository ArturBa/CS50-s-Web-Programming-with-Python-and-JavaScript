from django import forms


class PostForm(forms.Form):
    user = forms.IntegerField()
    message = forms.CharField(widget=forms.Textarea)
    topic = forms.IntegerField()
