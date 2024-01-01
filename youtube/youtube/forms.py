from django.forms import ModelForm

from .models import Video


class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'source', 'likes', 'views']
        # fields = ['title', 'description', 'source']
