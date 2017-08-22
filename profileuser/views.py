from django.shortcuts import render
from blog import models
from datetime import datetime
import time


def out_profile_user(request, id):
    min_5 = 300 # 300 second = 5 min

    update_activity(request)
    if request.user.is_authenticated():
        user = models.UserProfile.objects.get(user_id=request.user.id)
        auth = True
    this_user = models.UserProfile.objects.get(id=id)
    namepage = this_user.user.username
    if time.time() - this_user.last_activity <= min_5:
        Online = True
    else:
        loctime = time.strftime('%d.%m %H:%M:%S', time.localtime(this_user.last_activity))
    if request.user.is_authenticated():
        auth = True
        if int(request.user.id) == int(id):
            its_me = True
    playlists = models.Playlist.objects.filter(author=this_user)
    posts = models.Post.objects.filter(author=this_user)
    return render(request, 'profileuser/userpage.html', locals())



def edit_profile_user(request, id):
    pass


def update_activity(request):
    if request.user.is_authenticated():
        user = models.UserProfile.objects.get(user_id=request.user.id)
        user.last_activity = time.time()#models.timezone.now()
        user.save(update_fields=['last_activity',])