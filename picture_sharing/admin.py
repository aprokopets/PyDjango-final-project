from django.contrib import admin
from picture_sharing.models import Picture, Like

# Register your models here.

@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    pass
    
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass