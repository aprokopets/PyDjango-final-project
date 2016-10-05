from django.shortcuts import render, redirect
from django import forms
from picture_sharing.models import Picture, Like
from django.http import HttpResponse
from django.db.models import F

from django.conf import settings
import os
import final_project.settings

# -*- coding: utf8 -*-
# Create your views here.

_info = ''

class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()
    description = forms.CharField(max_length=100, label='Description', initial='Test description')



"""  Main page  """
def index(request):
    global _info
    copy_info = _info #take the info to show user
    _info = ''        #cleaning info
    
    #print(settings.BASE_DIR)
    #print(settings.MEDIA_ROOT)

    p = Picture.objects.order_by('-date_created')[:12]
    ctx = {'pictures' : p }
    ctx['info'] = copy_info
    ctx['page_title'] = 'Recent images(by date)'
    ctx['active_tab'] = 'main'
    return render(request, 'index.html', ctx)

""" Popular """
def popular(request):
    global _info
    copy_info = _info #take the info to show user
    _info = ''        #cleaning info
    
    p = Picture.objects.order_by('-views_count')[:12]
    ctx = {'pictures' : p }
    ctx['info'] = copy_info
    ctx['page_title'] = 'Popular images(by views)'
    ctx['active_tab'] = 'popular'
    return render(request, 'index.html', ctx)
    
""" Add image """
def add(request):
    global _info
    copy_info = _info #take the info to show user
    _info = ''        #cleaning info
    
    ctx = {}
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            obj = Picture.create(image=form.cleaned_data['image'], description=form.cleaned_data['description'])
            _info = 'image upload success'
            l = Like(id=obj)
            l.save()
            return redirect('/' + str(obj.key))
    else:
        ctx['info'] = copy_info
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
            global _info
            _info = 'Error...  '+str(e)+'   The key is: "'+str(key)+'"'
        p.views_count = F('views_count') + 1 #increase views counter
        p.save()

        p = Picture.objects.get(key=key)
        ctx['key']= p.key
        ctx['image'] =  p.image
        ctx['description'] = p.description
        ctx['date_created'] = p.date_created
        ctx['views_count'] = p.views_count
        ctx['page_title'] = 'Image properties'
        ctx['image_info'] = str(key)
        return render(request, 'image.html', ctx)
    except Exception as e:
        global _info
        _info = 'Error...  '+str(e)+'   The key is: "'+str(key)+'"'
        return redirect('/')

"""Delete image"""
def delete(request, key):
    try:
        obj = Picture.objects.get(key=key)
        print(str(settings.MEDIA_ROOT) + str(obj.image))
        os.remove(str(settings.MEDIA_ROOT) + '\\' + str(obj.image))
        obj.delete()
        
        return redirect('/')
    except Exception as e:
        global _info
        _info = 'Error...  '+str(e)+'   The key is: "'+str(key)+'"'
        return redirect('/')

""" Add like to image """
def like(request, key):
    # уточнить, как можно обойти здесь auto_now
    try:
        p = Picture.objects.get(key=key)
        l = Like.objects.get(id=p.id)
        l.likes = F('likes') + 1
        l.save()
        return redirect('/' + str(key))
    except Exception as e:
        global _info
        _info = 'Error...  '+str(e)+'   The key is: "'+str(key)+'"'
        return redirect('/')
        
"""  User images  """
def private(request):
    global _info
    copy_info = _info #take the info to show user
    _info = ''        #cleaning info
    
    #print(settings.BASE_DIR)
    #print(settings.MEDIA_ROOT)
    if request.user.is_authenticated():
        p = Picture.objects.order_by('-date_created')[:12]
        ctx = {'pictures' : p }
        ctx['info'] = copy_info
        ctx['page_title'] = 'Recent images(by date)'
        ctx['active_tab'] = 'private'
        ctx['private'] = True
        return render(request, 'index.html', ctx)
    else:
        return redirect('/')