from models import *
from django.forms import Form, ModelForm, ValidationError
from django.conf import settings
from re import sub
from django_magic.funcs import *

class NewPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('location', 'content', 'image') 
    def clean_content(self):
        content = self.cleaned_data['content']
        if content:
            return content[:settings.MAX_CONTENT_LENGTH]
        return content
    def clean_image(self):
        image = self.cleaned_data['image']
        if image and not is_valid_file(image.temporary_file_path()):
            raise ValidationError("Invalid file type.")
        return image

class CommentForm(ModelForm):
    class Meta:
        model = PostComment
        fields = ('content',)

    def clean_content(self):
        content = self.cleaned_data['content']
        if content: 
            return sub(r'\r\n|\r|\n', ' ', content)[:settings.MAX_CONTENT_LENGTH]
        return content
