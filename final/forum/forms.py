from django import forms


class PostForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)
    topic = forms.IntegerField()


class PointForm(forms.Form):
    post = forms.IntegerField()


class TopicForm(forms.Form):
    theme = forms.IntegerField()
    topic = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)
