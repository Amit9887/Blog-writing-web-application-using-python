from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(LikeComment)
admin.site.register(User_detail)
