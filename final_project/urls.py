"""final_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from picture_sharing import views
from django.conf.urls import static
from final_project import settings
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^login/$', auth_views.login),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}),
    url('^', include('django.contrib.auth.urls')),
    url(r'^$', views.index),
    url(r'^popular', views.popular),
    url(r'^add', views.add),
    url(r'^private$', views.private),
    url(r'^delete/(\w+)', views.delete),
    url(r'^like/(\w+)', views.like),
    url(r'^admin', admin.site.urls),
    url(r'^(?P<key>\w+)$', views.show_image, name='image'),
]

if settings.DEBUG:
        from django.conf.urls.static import static
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)