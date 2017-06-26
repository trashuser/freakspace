from django.shortcuts import render, get_object_or_404
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
    update_views_playlist()
    return render(request, 'blog/playlist.html', locals())

def output_single_pubish(request, id):
    post = Post.objects.get(id=id)
    post.views += 1
    post.save(update_fields=['views'])
    return render(request, 'blog/single.html', locals())

def update_views_playlist():
    playlist = Playlist.objects.all()
    for list in playlist:
        posts = list.post_set.all()
        views = 0
        for post in posts:
            views += post.views
        # if list.views < views:
        list.views = views
        list.save(update_fields=['views'])

