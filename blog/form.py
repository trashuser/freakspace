from django.forms import ModelForm
from .models import Post, Playlist

class WritePost(ModelForm):
    class Meta:
        model = Post
        fields = ['post_img',]

class CreatePlaylist(ModelForm):
    class Meta:
        model = Playlist
        fields = ['main_img']
