from django.contrib import admin
from .models import *
# Register your models here.
class AdminPost(admin.ModelAdmin):
    list_display = ('title' , 'price' , 'category' , 'sub_category' ,'cover')
admin.site.register(Post , AdminPost)

admin.site.register(Pro)

admin.site.register(Comment)

admin.site.register(Profile)

admin.site.register(Blog)
admin.site.register(Tag)