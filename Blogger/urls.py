
from django.contrib import admin
from django.urls import path
from Blog.views import *
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Home,name = 'home'),
    path('about/',About,name = 'about'),
path('login/',Login,name = 'login'),
path('signup/',Signup,name = 'signup'),
path('logout/',Logout,name = 'logout'),
path('myblog/', MyBlog, name='myblog'),
path('addblog/', AddBlog, name='addblog'),
path('change_image/', Change_image, name='change'),
path('change_pwd/', Change_password, name='change_pwd'),
    path('blog_detail/<int:bid>',Blog_detail,name='detail'),
path('blog_like/<int:pid>',Like_post,name='like'),
path('blog_comment/<int:pid>',Post_comment,name='comment'),
    path('blog_delete/<int:bid>',Blog_delete,name='b_delete'),
    path('cat_detail/<int:cid>/',Category_detail,name='cat_detail')
]+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
