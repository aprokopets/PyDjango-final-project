from django.shortcuts import render, redirect
from django import forms
from picture_sharing.models import Picture, Like
from django.http import HttpResponse
from django.db.models import F
from django.contrib import messages
try:
    from django.utils import simplejson as json
except ImportError:
    import json


from django.conf import settings
import os
import final_project.settings

# -*- coding: utf8 -*-
# Create your views here.

class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()
    description = forms.CharField(max_length=100, label='Description', initial='Test description')



"""  Main page  """
def index(request):
    
    p = Picture.objects.order_by('-date_created')[:12]
    ctx = {'pictures' : p }
    ctx['page_title'] = 'Recent images(by date)'
    ctx['active_tab'] = 'main'
    return render(request, 'index.html', ctx)

""" Popular """
def popular(request):
    
    p = Picture.objects.order_by('-views_count')[:12]
    ctx = {'pictures' : p }
    ctx['page_title'] = 'Popular images(by views)'
    ctx['active_tab'] = 'popular'
    return render(request, 'index.html', ctx)
    
""" Add image """
def add(request):
    
    ctx = {}
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if request.user.is_authenticated():
            user = str(request.user)
        else:
            user = 'anonymous'
        if form.is_valid():
            obj = Picture.create(image=form.cleaned_data['image'], description=form.cleaned_data['description'], user=user)
            messages.success(request, 'image upload success')
            l = Like(id=obj)
            l.save()
            
            
            
            return redirect('/' + str(obj.key))
    else:
        ctx['page_title'] = 'Add images'
        ctx['active_tab'] = 'add'
        return render(request, 'add.html', ctx)

""" Display one image and all its info """
def show_image(request, key):
    try:
        p = Picture.objects.get(key=key)
        ctx = {}
        ctx['date_last_view'] = p.date_last_view
        try:
            l = Like.objects.get(id=p.id)
            ctx['likes'] = l.likes
        except Exception as e:
            messages.error(request, 'Error...  '+str(e)+'   The key is: "'+str(key)+'"')
        p.views_count = F('views_count') + 1 #increase views counter
        p.save()

        p = Picture.objects.get(key=key)
        ctx['picture'] = p
        ctx['page_title'] = 'Image properties'
        ctx['image_info'] = str(key)
        return render(request, 'image.html', ctx)
    except Exception as e:
        
        messages.error(request, 'Error...  '+str(e)+'   The key is: "'+str(key)+'"')
        return redirect('/')

"""Delete image"""
def delete(request, key):
    try:
        obj = Picture.objects.get(key=key)
        print(str(settings.MEDIA_ROOT) + str(obj.image))
        if str(request.user) == str(obj.user):
            os.remove(str(settings.MEDIA_ROOT) + '\\' + str(obj.image))
            obj.delete()
        else:
            messages.error(request, 'You can not delete picture of user '+ str(obj.user) + ' because you are ' + str(request.user))
        return redirect('/')
    except Exception as e:
        messages.error(request, 'Error...  '+str(e)+'   The key is: "'+str(key)+'"')
        return redirect('/')

""" Add like to image """
def like(request):
    if request.method == "POST":
        rkey = request.POST.get('key', None)
        print('rkey = ' + rkey)
    
    try:
        p = Picture.objects.get(key=rkey)
        l = Like.objects.get(id=p.id)
        l.likes = F('likes') + 1
        l.save()
        print('Success')
        l = Like.objects.get(id=p.id)
        ctx = {}
        ctx['message'] = "You liked it"
        ctx['likes_count'] = l.likes
        return HttpResponse(json.dumps(ctx), content_type='application/json')
        #return redirect('/' + str(key))
    except Exception as e:
        print('Exception')
        messages.error(request, 'Error...  '+str(e)+'   The key is: "'+str(rkey)+'"')
        return redirect('/')
        
"""  User images  """
def private(request):
    
    #print(settings.BASE_DIR)
    #print(settings.MEDIA_ROOT)
    if request.user.is_authenticated():
        p = Picture.objects.order_by('-date_created').filter(user=str(request.user))[:12]
        ctx = {'pictures' : p }
        ctx['page_title'] = 'Recent images(by date) of user: '+str(request.user)
        ctx['active_tab'] = 'private'
        ctx['private'] = True
        return render(request, 'index.html', ctx)
    else:
        p = Picture.objects.order_by('-date_created').filter(user='anonymous')[:12]
        ctx = {'pictures' : p }
        ctx['page_title'] = 'Recent images(by date)'
        ctx['active_tab'] = 'private'
        ctx['private'] = True
        return render(request, 'index.html', ctx)