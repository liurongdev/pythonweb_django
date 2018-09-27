

from django import forms

from .models import Topic ,Entry

class TopicForm(forms.ModelForm):
    """定义元数据信息"""
    class Meta:
        model=Topic
        fields=['text']
        labels={"text":''}


class EntryForm(forms.ModelForm):
    """定义元数据信息"""

    class Meta:
        model = Entry
        fields = ['text']
        labels = {"text": ''}
        widgets={"text": forms.Textarea(attrs={"color":80})}
