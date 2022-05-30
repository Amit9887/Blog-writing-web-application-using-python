from django.shortcuts import render,redirect

# Create your views here.
def All_category():
    all_cat = Category.objects.all()
    return all_cat
def Recent_and_popular():
    allpost = Post.objects.all()
    recent_three = allpost[::-1][:3]
    like = []
    le = len(allpost)
    newpost =[]
    for i in allpost:
        l = LikeComment.objects.filter(post_data = i,like = True).count()
        like.append(l)
    for i in range(le):
        if max(like)>0:
            m = max(like)
            p = like.index(m)
            po = allpost[p]
            like.pop(p)
            like.insert(p,0)
            newpost.append(po)
    top_three = newpost[:3]
    return top_three,recent_three


from .models import *
def Home(request):

    allpost = Post.objects.all()
    li = []
    for i in allpost:
        like = LikeComment.objects.filter(post_data = i,like = True).count()
        li.append(like)

    z = zip(allpost,li)
    top3,recent3 = Recent_and_popular()
    d = {"allcat":All_category(),"allpost":z,"top3":top3,
         "recent3":recent3}
    return render(request,'index.html',d)

def About(request):
    d = {"allcat":All_category()}
    return render(request,'about.html',d)
from django.contrib.auth import authenticate,login,logout
def Login(request):
    error = False
    if request.method == "POST":
        dd = request.POST
        u = dd['user']
        p = dd['pwd']
        user = authenticate(username = u,password = p)
        if user:
            login(request,user)
            return redirect('home')
        else:
            error = True

    d = {"allcat": All_category(),"error":error}
    return render(request,'login.html',d)


def Blog_detail(request,bid):
    blog_data = Post.objects.get(id = bid)
    d = {"allcat": All_category(),"detail":blog_data}
    return render(request,'singlepage.html',d)


def Like_post(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    data = Post.objects.get(id = pid)
    data2 = LikeComment.objects.filter(usr = request.user,
                                       like = True,post_data=data)
    if not data2:
        data3 = LikeComment.objects.filter(post_data = data,
                                           usr = request.user).first()
        if data3:
            data3.like = True
            data3.save()
        else:
            LikeComment.objects.create(post_data = data,
                                       usr = request.user,
                                   like = True)
            return redirect('home')
    else:
        return redirect('home')

def Signup(request):
    error = False

    if request.method == "POST":
        dd = request.POST
        n = dd['name']
        u = dd['user']
        e = dd['em']
        p = dd['pwd']
        i = request.FILES['img']
        udata = User.objects.filter(username = u)
        if udata:
            error = True
        else:
            user = User.objects.create_user(username = u,password = p,email = e,
                                first_name = n)
            User_detail.objects.create(usr = user,image = i)
            return redirect('login')
    d = {"allcat": All_category(),"error":error}

    return render(request,'signup.html',d)

def Logout(request):
    logout(request)
    return redirect('login')
from datetime import date
def Post_comment(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    pdata = Post.objects.get(id = pid)
    user = request.user
    td = date.today()
    if request.method=="POST":
        d = request.POST
        c = d['Message']
        data = LikeComment.objects.filter(usr = request.user,
                                          post_data = pdata).first()
        if data:
            data.comment = c
            data.save()
        else:
            LikeComment.objects.create(usr = user,post_data = pdata
                                       ,comment = c,date = td)
    return redirect('detail',pid)

def MyBlog(request):
    data = Post.objects.filter(usr = request.user)
    d = {"allcat": All_category(),"data":data}
    return render(request,'fashion.html',d)

def Blog_delete(request,bid):
    data = Post.objects.get(id = bid)
    data.delete()
    return redirect('myblog')

def Category_detail(request,cid):
    cdata = Category.objects.get(id = cid)
    d = {"cdata":cdata}
    return render(request,'detail.html',d)

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings
def AddBlog(request):
    if request.method == "POST":
        dd = request.POST
        t = dd['title']
        i = request.FILES['img']
        st = dd['short']
        lt = dd['long']
        c = dd['cat']
        cdata = Category.objects.get(id = c)
        user = request.user
        td = date.today()
        Post.objects.create(cat = cdata,usr = user,title = t,
                            short_des = st,long_des = lt,date = td,image = i)
        from_email = settings.EMAIL_HOST_USER
        to_email = user.email
        sub = "Blog Added"
        msg = EmailMultiAlternatives(sub,'',from_email,[to_email])
        dic = {"title":t,"des":st}
        html = get_template('mail.html').render(dic)
        msg.attach_alternative(html,'text/html')
        msg.send()
        return redirect('myblog')

    d = {"allcat":All_category()}
    return render(request,'add_blog.html',d)

def Change_image(request):
    udata = User_detail.objects.filter(usr = request.user).first()
    if request.method == "POST":
        i = request.FILES['img']
        udata.image = i
        udata.save()
        return redirect('myblog')
    d = {"udata":udata}
    return render(request,'change_image.html',d)

def Change_password(request):
    if request.method == "POST":
        o = request.POST['old']
        n = request.POST['new']
        data = authenticate(username = request.user.username,password = o)
        if data:
            data.set_password(n)
            data.save()
            logout(request)
            login(request,data)
            return redirect('myblog')
    return render(request,'change_pwd.html')