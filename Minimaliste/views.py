from django.shortcuts import render , redirect ,get_object_or_404
from django.http import HttpResponse

from django.urls import reverse

from django.core.paginator import Paginator

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout

from .models import *

from .decorators import unauthenticated_user , paied_users
from django.contrib.auth.decorators import login_required ,permission_required

from .forms import *

from .filters import *

from datetime import datetime , date , timedelta

import stripe


#setting stripe code
from .apiKeys import code
from django.db.models import Min ,Max
stripe.api_key = code

def ispro(request):
    isPro = False
    try :
        if request.user.is_authenticated:
            pro = Pro.objects.get(user = request.user)
            isPro = pro.has_paid
            if not isPro:
                pro.delete()
    except:
        isPro = False

    return isPro



# Create your views here.
def home(request):
    admin = request.user.groups.filter(name="admins").exists()
    posts = Post.objects.all().order_by('-id')

    isPro = ispro(request)

    minMaxPrice = Post.objects.aggregate(Min('price') ,Max('price'))

    myFilter = PostFilter(request.GET , queryset=posts)
    posts = myFilter.qs
    sub_category = request.GET.get("sub_category")
    if sub_category:
        posts = myFilter.qs
    maxPrice = request.GET.get('maxPrice')

    if maxPrice:
        posts = posts.filter(price__lte=maxPrice)


    context={
        'minMaxPrice':minMaxPrice,
        'myFilter' : myFilter ,
        'posts':posts ,
        'admin' : admin ,
        'isPro' : isPro ,
        #'paginator' : paginator,
        }
    return render(request , 'home.html' , context)


def shop(request):
    admin = request.user.groups.filter(name="admins").exists()
    posts = Post.objects.all().order_by('-id')

    isPro = ispro(request)

    minMaxPrice = Post.objects.aggregate(Min('price') ,Max('price'))

    myFilter = PostFilter(request.GET , queryset=posts)
    posts = myFilter.qs

    tri = request.GET.get('tri')
    if tri :
        tri = int(tri)
        if tri == 1:
            posts = Post.objects.all().order_by('-id')
        elif tri == 2:
            posts = Post.objects.all().order_by('id')
        elif tri == 3:
            posts = Post.objects.all().order_by('price')
        elif tri == 4:
            posts = Post.objects.all().order_by('-price')

    sub_category = request.GET.get("sub_category")
    if sub_category:
        posts = myFilter.qs

    sub_sub = request.GET.get("sub_sub")
    if sub_sub:
        posts = myFilter.qs

    maxPrice = request.GET.get('maxPrice')
    if maxPrice:
        posts = myFilter.qs
        posts = posts.filter(price__lte=maxPrice)

    paginator = Paginator(posts , 30)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    context={
        'minMaxPrice':minMaxPrice,
        'myFilter':myFilter,
        'posts':posts ,
        'admin' : admin ,
        'isPro' : isPro ,
        'paginator' : paginator,
        'maxPrice':maxPrice,
        }
    return render(request , 'shop.html' , context)


def filterbycat(request , cat):
    admin = request.user.groups.filter(name="admins").exists()
    posts = Post.objects.filter(category__contains =cat).order_by('-id')


    minMaxPrice = Post.objects.aggregate(Min('price') ,Max('price'))

    myFilter = PostFilter(request.GET , queryset=posts)

    posts = myFilter.qs

    tri = request.GET.get('tri')
    if tri :
        tri = int(tri)
        if tri == 1:
            posts = Post.objects.filter(category__contains =cat).order_by('-id')
        elif tri == 2:
            posts = Post.objects.filter(category__contains =cat).order_by('id')
        elif tri == 3:
            posts = Post.objects.filter(category__contains =cat).order_by('price')
        elif tri == 4:
            posts = Post.objects.filter(category__contains =cat).order_by('-price')

    maxPrice = request.GET.get('maxPrice')
    if maxPrice:
        posts = posts.filter(price__lte=maxPrice)


    isPro = ispro(request)

    paginator = Paginator(posts , 30)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    context={
        'minMaxPrice':minMaxPrice,
        'myFilter':myFilter,
        'posts':posts ,
        'admin' : admin ,
        'isPro' : isPro ,
        'maxPrice':maxPrice,
        'paginator' : paginator,
        'cat':cat,
        }
    return render(request , 'shop.html', context)


def contact(request):
    return render(request , 'contact.html')


#Blog function !
def blog(request):
    posts = Blog.objects.all().order_by('-id')

    myFilter = BlogFilter(request.GET , queryset=posts)
    posts = myFilter.qs

    paginator = Paginator(posts , 30)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    context = {
        'myFilter':myFilter,
        'posts' : posts,
        'paginator':paginator,
    }
    return render(request ,  'blog/blog.html' , context)


def blogTag(request , pk):
    posts = Blog.objects.all().order_by('-id')
    tag = Tag.objects.get(pk = pk)

    tags = Tag.objects.all()

    paginator = Paginator(posts , 30)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    context = {
        'myFilter':myFilter,
        'posts' : posts,
        'paginator':paginator,
    }
    return render(request ,  'blog/blog.html' , context)

def viewBlogPage(request , pk):
    com = Comment()
    post = Blog.objects.get(pk=pk)

    if request.method == 'POST':
        com.body = request.POST.get('comment')
        com.user = request.user
        com.post = post
        com.save()

    comments = Comment.objects.filter(post = post).order_by('-commented_at')
    length = comments.count

    paginator = Paginator(comments , 6)
    page = request.GET.get('page')
    comments = paginator.get_page(page)

    context = {
        'post' : post ,
        'comments':comments,
        'length':length,
    }
    return render(request , 'blog/blogPost.html', context)


@login_required(login_url="login")
def deleteCom(request , pk):
    com = Comment.objects.get(pk = pk)
    c = com.post.id
    if request.user == com.user:
        com.delete()
        return redirect('viewblog',pk=c)


#users
@login_required(login_url="login")
def myProfile(request , pk):
    user = User.objects.get(username=pk)
    print(user)

    try:
        profile = get_object_or_404(Profile , user = user)
    except:
        return redirect('makeProfile', pk=user.username )

    context = {
        'user':user,
        'profile':profile,
        'myposts':myposts,
    }
    return render(request , 'user/profile.html',context)


@login_required(login_url="login")
def makeProfile(request,pk):
    if request.method == 'POST':
        profile = Profile()
        profile.user = request.user
        profile.firstname = request.POST.get('firstname')
        profile.lastname = request.POST.get('lastname')
        profile.birthday = request.POST.get('birthday')
        profile.image = request.FILES.get('image')
        profile.gender = request.POST.get('gender')
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        profile.save()
        return redirect('Profile',pk=request.user)

    return render(request , 'user/makeProfile.html')


@login_required(login_url="login")
def updateProfile(request , pk):
    profile = Profile.objects.get(pk = pk)

    if request.method == 'POST':
        profile.firstname = request.POST.get('firstname')
        profile.lastname = request.POST.get('lastname')
        profile.birthday = request.POST.get('birthday')
        profile.address = request.POST.get('address')
        profile.phone = request.POST.get('phone')
        profile.gender = request.POST.get('gender')
        img = request.FILES.get('avatar')
        if img :
            profile.image = img

        profile.save()
        return redirect('Profile', pk=request.user.username)

    context ={
        'profile' : profile ,
    }
    return render(request,'user/updateProfile.html' , context)

@login_required(login_url="login")
def myposts(request):
    posts = Post.objects.all().filter(user=request.user)

    minMaxPrice = Post.objects.aggregate(Min('price') ,Max('price'))

    myFilter = PostFilter(request.GET , queryset=posts)

    if request.method == 'GET':
        myFilter.form.title = request.GET.get('title')
        myFilter.form.pays = request.GET.get('pays')
        myFilter.form.ville = request.GET.get('ville')
        myFilter.form.category = request.GET.get('category')
        myFilter.form.sub_category = request.GET.get('sub_category')

    posts = myFilter.qs

    maxPrice = request.GET.get('maxPrice')
    if maxPrice:
        posts = posts.filter(price__lte=maxPrice)

    paginator = Paginator(posts , 15)
    page = request.GET.get('page')
    myposts = paginator.get_page(page)

    context  ={
        'myFilter':myFilter,
        'posts' : posts,
        'paginator':paginator,
        'maxPrice':maxPrice,
        'minMaxPrice':minMaxPrice,
    }
    return render(request , 'shop.html',context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request , username=username , password=password)

        if user is not None :
            login(request , user)
            return redirect('home')
        else:
            messages.info(request , 'username or password is incorrect')

    context = {}
    return render(request , 'accounts/signin.html',context)


@login_required(login_url="login")
def logoutUser(request):
    logout(request)
    return redirect('login')


def signupPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request , f'Account was added for {username}')
            return redirect('login')

    context = {'form' : form}
    return render(request , 'accounts/signup.html',context)


#Posts
@unauthenticated_user
@login_required(login_url="login")
def addPost(request):
    form = AddPostForm()

    if request.method == 'POST':
        form = AddPostForm(request.POST , request.FILES)
        post = Post()
        if form.is_valid():
            post.user = request.user
            post.title = form.cleaned_data.get('title')
            post.description = form.cleaned_data.get('description')
            post.shortDescription = form.cleaned_data.get('shortDescription')
            post.cover = form.cleaned_data.get('cover')
            post.category = form.cleaned_data.get('category')
            post.pays = form.cleaned_data.get('pays')
            post.ville = form.cleaned_data.get('ville')
            post.price = form.cleaned_data.get('price')
            post.phone = form.cleaned_data.get('phone')
            post.sub_category = form.cleaned_data.get('sub_category')
            post.sub_sub = form.cleaned_data.get("sub_sub")

            post.save()
            return redirect('shop')

    context = {
        "form" : form
    }
    return render(request , 'posts/addPost.html' , context)


def viewPost(request , pk):
    commentForm = CommentForm()
    post = Post.objects.get(pk = pk)
    if post.category == "Services" and not ispro(request) :
        return redirect("updateToPro")

    context = {
        'post' : post ,
    }
    return render(request , 'posts/viewpost.html',context)


@unauthenticated_user
@login_required(login_url="login")
def deletePost(request , pk):
    post = Post.objects.get(pk=pk)
    admin = User.objects.get(username="admin")
    if request.user in [post.user , admin]:
        post.delete()
        return redirect('shop')
    else:
        return HttpResponse("<h1>You are not the owner !</h1>")


@unauthenticated_user
def updatePost(request , pk ):
    post = Post.objects.get(pk=pk)
    form = AddPostForm(instance=post)

    if request.method == 'POST':
        form = AddPostForm(request.POST , request.FILES , instance=post)
        if form.is_valid():
            post.user = request.user
            post.title = form.cleaned_data.get('title')
            post.description = form.cleaned_data.get('description')
            post.shortDescription = form.cleaned_data.get('shortDescription')
            post.cover = form.cleaned_data.get('cover')
            post.category = form.cleaned_data.get('category')
            post.pays = form.cleaned_data.get('pays')
            post.ville = form.cleaned_data.get('ville')
            post.price = form.cleaned_data.get('price')
            post.phone = form.cleaned_data.get('phone')
            post.sub_category = form.cleaned_data.get('sub_category')
            post.sub_sub = form.cleaned_data.get("sub_sub")
            post.save()

            return redirect('viewpost' , pk=pk)

    context = {
        'form' : form ,
    }
    return render(request , 'posts/addPost.html',context)



@login_required(login_url='login')
def payment(request):
    request.user.groups.clear()
    request.user.groups.add(2)
    return redirect('home')


@login_required(login_url="login")
def updateToPro(request):
    isPro = ispro(request)
    if isPro:
        return render(request , "pro.html")
    context = {
        'isPro':isPro ,
    }
    return render(request , 'accounts/acc-pro.html' , context)


@login_required(login_url='login')
def charge(request):
    today = date.today()
    print(today)

    if request.method == 'POST':
        pro = Pro()
        pro.user = request.user
        pro.siret = request.POST.get('siret')
        pro.startupName = request.POST.get('startupName')
        pro.skills = request.POST.get('skills')
        pro.codePostal = request.POST.get('codePostal')
        pro.phone = request.POST.get('phone')

        amount = int ( request.POST.get('amount') )
        if amount == 5 :
            lastdate = today + timedelta(days=30)
        elif amount == 10 :
            lastdate = today + timedelta(days=30 * 3)
        elif amount == 25 :
            lastdate =  today + timedelta(days=30 * 6 )
        pro.paid_until = lastdate
        pro.save()

        customer = stripe.Customer.create(
            email = request.user.email ,
            name = request.user.username ,
            source = request.POST['stripeToken'],
        )

        charge = stripe.Charge.create(
            customer = customer,
            amount =  amount * 100 ,
            currency = 'eur',
            description = f'Update to Pro until {lastdate} '
        )
        print('data : ' , request.POST)

    return redirect(reverse('success' , args=[amount] ))


@login_required(login_url='login')
def successMsg(request , args):
    amount = args

    context = {
        'amount' : amount
    }
    return render(request , 'thankyouPage.html',context)