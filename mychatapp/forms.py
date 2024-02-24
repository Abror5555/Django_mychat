from django import forms
from django.forms import ModelForm
from mychatapp.models import ChatMessage

class ChatMessageForm(ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 3, "placeholder":"Type your message here!"}))
    class Meta:
        model = ChatMessage
        fields = ["body",]