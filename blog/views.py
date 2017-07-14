from django.shortcuts import render, render_to_response, redirect
from .models import *
from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
# from django.core.context_processors import csrf


def output_publish(request):
    update_activity(request)
    update_numb_tags()
    top_playlist = Playlist.objects.order_by('-like')[:4]
    posts = Post.objects.order_by('-created_date')[:20]
    auth = False
    carousel = Post.objects.order_by('-like')[:4]
    active_slide = carousel[0]
    carousel = carousel[1:4]
    top_tags = Tag.objects.order_by('-numb')[:20]
    if request.user.is_authenticated():
        user = UserProfile.objects.get(user_id=request.user.id)
        auth = True
    # posts.reverse()
    return render_to_response('blog/index.html', locals())



def output_tags(request, tag):
    title = tag
    posts = Post.objects.filter(tags=Tag.objects.get(name=tag).id)
    return render(request, 'blog/posts.html', locals())



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
    comments = Comment.objects.filter(post=post)
    tags = Tag.objects.filter(post=id)
    for tag in tags:
        tag.numb = Post.objects.filter(tags__name__startswith=tag.name).count()

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
    update_views_playlist()
    return render(request, 'blog/single.html', locals())


@csrf_protect
def add_comment(request, post_id):
    if request.POST:

        comment = Comment(content=request.POST.get('comment', ''),
                          author=UserProfile.objects.get(user=request.user),
                          post=Post.objects.get(id=post_id))
        comment.save()
        return redirect('/post/id'+post_id+'#comment')



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



#      UPDATE
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




def update_activity(request):
    if request.user.is_authenticated():
        user = UserProfile.objects.get(user_id=request.user.id)
        user.last_activity = time.time()
        user.save(update_fields=['last_activity',])



def update_numb_tags():
    tags = Tag.objects.all()
    for tag in tags:
        tag.numb = Post.objects.filter(tags__name__startswith=tag.name).count()
        tag.save()