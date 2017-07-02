from django.shortcuts import render
from .models import *
from django.http import Http404, JsonResponse

def output_publish(request):
    posts = Post.objects.order_by('-created_date')
    # posts.reverse()
    return render(request, 'blog/index.html', locals())

# def output_tags(request, tag):
#     tagi = tag
#     posts = Post.objects.all()
#     return render(request, 'blog/playlist.html', locals())

def output_playlist(request, id):
    update_views_playlist()
    playlist = Playlist.objects.select_related().get(id=id)
    posts = playlist.post_set.all()
    return render(request, 'blog/playlist.html', locals())

def output_single_pubish(request, id):
    post = Post.objects.get(id=id)
    post.views += 1
    post.save(update_fields=['views'])
    auth = False
    if request.user.is_authenticated():
        user = UserProfile.objects.get(user_id=request.user)
        auth = True
        push_like = False
        you_post = False
        liking = post.liking.select_related()
        if post.author.user != user.user:
            for liker in liking:
                if liker == user.user:
                    push_like = True
        else:
            you_post = True
    return render(request, 'blog/single.html', locals())


def update_views_playlist():
    playlist = Playlist.objects.all()
    for list in playlist:
        posts = list.post_set.all()
        views = like = 0
        for post in posts:
            views += post.views
            like += post.like
        # if list.views < views:
        list.views = views
        list.like = like
        list.save(update_fields=['views', 'like'])

def add_ajax(request, id):
    if request.is_ajax():

        like = Post.objects.get(id=id)
        user = UserProfile.objects.get(user_id=request.user.id)

        liking = like.liking.select_related()
        if like.author.user != user.user:
            for liker in liking:
                if liker == user.user:
                    return Http404
            user.like -= 1
            user.save(update_fields=['like'])

            like.liking.add(user.user)

            like.author.like += 1
            like.author.save(update_fields=['like'])
            like.like += 1
            like.save(update_fields=['like'])
            response = {'count-like': like.like, 'author-like': like.author.like}
            print(response)
            return JsonResponse(response)
        else:
            return Http404
