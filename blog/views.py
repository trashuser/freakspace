from django.shortcuts import render
from .models import *

def output_publish(request):
    posts = Post.objects.all()
    return render(request, 'blog/index.html', locals())

# def output_tags(request, tag):
#     tagi = tag
#     posts = Post.objects.all()
#     return render(request, 'blog/playlist.html', locals())

def output_playlist(request, id):
    playlist = Playlist.objects.select_related().get(id=id)
    posts = playlist.post_set.all()
    return render(request, 'blog/playlist.html', locals())

