# forms.py
from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Введите ваше сообщение...'}),
        }
        labels = {
            'content': ''
        }


from django import forms
from .models import Files

class FileForm(forms.ModelForm):
    class Meta:
        model = Files
        fields = ('file', 'themes')


