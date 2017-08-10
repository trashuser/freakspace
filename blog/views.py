from django.shortcuts import render, render_to_response, redirect
from .models import *
from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .form import *
# from django.core.context_processors import csrf


def output_publish(request):
    update_activity(request)
    # update_numb_tags()

    top_playlist = Playlist.objects.order_by('-like')[:4]

    posts = Post.objects.order_by('-created_date')[:20]
    for post in posts:
        post.comments_numb = Comment.objects.filter(post=post).count()

    carousel = Slider.objects.filter(is_active='1')
    active_slide = carousel[0]
    carousel = carousel[1:]

    top_tags = Tag.objects.order_by('-numb')[:15]

    if request.user.is_authenticated():
        user = UserProfile.objects.get(user_id=request.user.id)
        auth = True

    return render_to_response('blog/index.html', locals())



def output_tags(request, tag):
    title = tag
    posts = Post.objects.filter(tags=Tag.objects.get(name=tag).id)
    for post in posts:
        post.comments_numb = Comment.objects.filter(post=post).count()
    return render(request, 'blog/posts.html', locals())



def output_playlist(request, id):
    update_activity(request)
    update_views_playlist(id)
    update_comments(id)
    playlist = Playlist.objects.select_related().get(id=id)
    color = playlist.color
    if playlist.author == UserProfile.objects.get(user=request.user) or request.user.is_superuser:
        edit_playlist = True
    posts = playlist.post_set.all()
    for post in posts:
        post.comments_numb = Comment.objects.filter(post=post).count()

    auth = False
    if request.user.is_authenticated():
        user = UserProfile.objects.get(user=request.user)
        auth = True

    return render(request, 'blog/playlist.html', locals())



def output_single_pubish(request, id):
    update_activity(request)
    auth = False
    is_admin = False
    post = Post.objects.get(id=id)
    post.views += 1
    post.save(update_fields=['views'])
    comments = Comment.objects.filter(post=post)
    comments.numb = comments.count()
    tags = Tag.objects.filter(post=id)
    for tag in tags:
        tag.numb = Post.objects.filter(tags__name__startswith=tag.name).count()
    try:
        playlist = Playlist.objects.get(post=post)
    except:
        pass
    else:
        post_in_playlists = Post.objects.filter(playlist_id=playlist.id).order_by('published_date')

    if request.user.is_authenticated():
        user = UserProfile.objects.get(user=request.user)
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
        if request.user.is_superuser:
            is_admin = True
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





# WRITE AND EDIT POST
def write_post(request, id_post=None):
    auth = False

    # user auth?
    if request.user.is_authenticated():
        this_admin = False
        this_user = False
        selected_playlist = False
        auth = True
        is_edit = False

        user = UserProfile.objects.get(user_id=request.user)

        try:
            post = Post.objects.get(id=id_post)
        except:
            pass
        else:
            # is author?
            if post.author == user:
                this_user = True

        # is admin?
        if request.user.is_superuser:
            this_admin = True

        # render playlist
        # if this_admin:
        #     playlists = Playlist.objects.all()
        # else:
        playlists = Playlist.objects.filter(
            author=UserProfile.objects.get(user=request.user)
        )


        # render value if edit post and user auth or this is admin
        if id_post and (this_user or this_admin):
            is_edit = True
            post = Post.objects.get(id=id_post)
            val_title = post.title
            val_text = post.text

            # out tags
            __tags = Tag.objects.filter(post=id_post)
            __tags_array = []
            for tag in __tags:
                __tags_array.append(tag.name)
            tag_val = ', '.join(__tags_array)


            selected_playlist = post.playlist
            for playlist in playlists:
                if str(playlist.name) == str(selected_playlist):
                    playlist.selected = True

        elif id_post and (not this_user and not this_admin):
            return redirect('/post/id'+str(id_post))

        form = WritePost()
        return render(request, 'blog/write.html', locals())

    # if user don`t auth - redirect to page login
    else:
        return redirect('/auth/login/')


def create_playlist(request, id_playlist=None):
    if not request.user.is_authenticated():
        return redirect('/auth/login/')
    auth = True
    colors = ['14dc52', '69a02d', '175d0b', '0d91bb', '2f6475',
              '0d3744', 'e0d123', 'e06923', 'e04623']
    if id_playlist:
        playlist = Playlist.objects.get(id=id_playlist)
        if playlist.author == UserProfile.objects.get(user=request.user) or request.user.is_superuser:
            val_name = playlist.name
            val_description = playlist.description
            selected_color = playlist.color.lstrip('#')
            edit_playlist = True
        else:
            return redirect('/playlist/id'+id_playlist)

    form = CreatePlaylist()
    return render(request, 'blog/createPlaylist.html', locals())

@csrf_protect
def commit_playlist(request):
    if request.POST:
        img_field = CreatePlaylist(request.POST, request.FILES)
        if img_field.is_valid():
            playlist = img_field.save(commit=False)
            playlist.name = request.POST.get('name')
            playlist.color = request.POST.get('selectbgcolor')
            print(playlist.color)
            playlist.description = request.POST.get('description')
            playlist.author = UserProfile.objects.get(user=request.user)
            playlist.save()
        return redirect('/playlist/id'+str(playlist.id))\

@csrf_protect
def commit_playlist_edit(request, id_playlist):
    if request.POST:
        playlist = Playlist.objects.get(id=id_playlist)

        img_field = CreatePlaylist(request.POST, request.FILES)
        if img_field.is_valid():
            bufer = img_field.save(commit=False)
            if bufer.main_img:
                playlist.main_img = bufer.main_img
        playlist.id = id_playlist
        playlist.name = request.POST.get('name')
        playlist.description = request.POST.get('description')
        playlist.color = request.POST.get('selectbgcolor')
        playlist.save()
        return redirect('/playlist/id'+str(playlist.id))



@csrf_protect
def add_post(request):
    if request.POST:
        post_form = WritePost(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.title = request.POST.get('title')
            post.text = request.POST.get('text')
            post.author = UserProfile.objects.get(user=request.user)
            post.published_date = timezone.now()
            try:
                post.playlist = Playlist.objects.get(id=request.POST.get('playlist'))
            except:
                pass
            post.save()
            row_tags = request.POST.get('tags').split(',')
            tags = [tag.strip() for tag in row_tags]
            for tag in tags:
                try:
                    this_tag = Tag.objects.get(name=tag)
                    post.tags.add(this_tag)

                except:
                    post.tags.create(name=tag)
                    this_tag = Tag.objects.get(name=tag)
                    this_tag.numb += 1
                    this_tag.save(update_fields=['numb'])
                else:
                    this_tag.numb += 1
                    this_tag.save(update_fields=['numb'])

            return redirect('/post/id' + str(post.id))
    else:
        return redirect('/')

@csrf_protect
def commit_post(request, id_post):
    if request.POST:
        post = Post.objects.get(id=id_post)

        post_form_img = WritePost(request.POST, request.FILES)
        if post_form_img.is_valid():
            bufer = post_form_img.save(commit=False)
            if bufer.post_img:
                post.post_img = bufer.post_img


        post.title = request.POST.get('title')
        post.text = request.POST.get('text')
        post.author = UserProfile.objects.get(user=request.user)
        post.published_date = timezone.now()
        post.playlist = Playlist.objects.get(id=request.POST.get('playlist'))
        post.save()
        row_tags = request.POST.get('tags').strip(',\n\r\t').split(',')
        tags = [tag.strip() for tag in row_tags if tag]
        post.tags.clear()
        post_tags = Tag.objects.filter(post=post)
        for tag in post_tags:
            if tag.name in tags:
                tags.remove(tag.name)

        for tag in tags:
            try:
                this_tag = Tag.objects.get(name=tag)
                post.tags.add(this_tag)

            except:
                post.tags.create(name=tag)
                this_tag = Tag.objects.get(name=tag)
                this_tag.numb += 1
                this_tag.save(update_fields=['numb'])
            else:
                this_tag.numb += 1
                this_tag.save(update_fields=['numb'])

        return redirect('/post/id' + str(post.id))
    else:
        return redirect('/')


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
def update_views_playlist(id=None):
    if not id:
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
    else:
        playlist = Playlist.objects.get(id=id)
        posts = playlist.post_set.all()
        views = like = 0
        for post in posts:
            views += post.views
            like += post.like
        # if list.views < views:
        playlist.views = views
        playlist.like = like
        playlist.save(update_fields=['views', 'like'])



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

def update_comments(id):
    playlist = Playlist.objects.get(id=id)
    posts = Post.objects.filter(playlist=playlist)
    comments = 0
    for post in posts:
        comments += Comment.objects.filter(post=post).count()

    playlist.comments = comments
    playlist.save(update_fields=['comments'])