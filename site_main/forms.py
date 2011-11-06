from models import *
from django.forms import Form, ModelForm
from re import sub

class CommentForm(ModelForm):
    class Meta:
        model = PostComment
        fields = ('content',)

    def clean_content(self):
        content = self.cleaned_data['content']
        return sub(r'\r\n|\r|\n', ' ', content)
