from django.shortcuts import render, render_to_response
from .models import *
from django.http import Http404, JsonResponse
# from django.core.context_processors import csrf


def output_publish(request):
    update_activity(request)
    posts = Post.objects.order_by('-created_date')
    auth = False
    if request.user.is_authenticated():
        user = UserProfile.objects.get(user_id=request.user.id)
        auth = True
    # posts.reverse()
    return render_to_response('blog/index.html', locals())

# def output_tags(request, tag):
#     tagi = tag
#     posts = Post.objects.all()
#     return render(request, 'blog/playlist.html', locals())

def output_playlist(request, id):
    update_activity(request)
    update_views_playlist()
    playlist = Playlist.objects.select_related().get(id=id)
    posts = playlist.post_set.all()
    auth = False
    if request.user.is_authenticated():
        user = UserProfile.objects.get(user_id=request.user)
        auth = True

    return render(request, 'blog/playlist.html', locals())

def output_single_pubish(request, id):
    update_activity(request)
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
        update_activity(request)

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
            return JsonResponse(response)
        else:
            return Http404


def update_activity(request):
    if request.user.is_authenticated():
        user = UserProfile.objects.get(user_id=request.user.id)
        user.last_activity = time.time()
        user.save(update_fields=['last_activity',])