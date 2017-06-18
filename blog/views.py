from django.shortcuts import render
from .models import *

def output_publish(request):
    posts = Post.objects.all()
    return render(request, 'blog/index.html', locals())