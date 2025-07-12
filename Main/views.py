from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import Http404
from . models import FeedPost,  FeedPostComment
User = get_user_model()

# Create your views here.

def public_homepage(request):
    return render(request, 'Main/pages/public_homepage.html')

@login_required
def home(request):
    return render(request, 'Main/pages/home.html')


def user_login(request):
    error = None
    if request.method == 'POST':
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')
        
        # Check if the input is an email
        if '@' in username_or_email:
            try:
                user = User.objects.get(email=username_or_email)
                username = user.username
            except User.DoesNotExist:
                username = username_or_email  # This will fail auth, which is fine
        else:
            username = username_or_email
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error = 'Invalid username/email or password'
            return render(request, 'Main/userAuth/user_login.html', {'error': error})
    
    return render(request, 'Main/userAuth/user_login.html', )

def user_signup(request):
    user_error = None
    email_error = None
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(fullname,username,password,email)
        
        if User.objects.filter(username=username).exists():
            user_error = 'Username already exists. Try another one.'
        elif User.objects.filter(email=email).exists():
            email_error = 'Email already registered. Try logging in.'
        else:
            user =  User.objects.create_user(
                 username=username,
                 email=email,
                 password=password,
             )
            user.fullname = fullname
            user.save()
            return redirect('login')

    return render(request, 'Main/userAuth/user_register.html', {'user_error':user_error, 'email_error':email_error} )


@login_required
def user_logout(request):
    logout(request)
    return redirect('welcome')


def about(request):
    return render(request, 'Main/pages/about1.html')



# --------------------FEED POST--------------------
# --------------------FEED POST--------------------
@login_required
def feed_post(request):
    if request.method == 'POST':
        caption = request.POST.get('caption')
        image = request.FILES.get('image')

        if caption or image:
            FeedPost.objects.create(
                caption = caption,
                image = image,
                author=request.user,
            )
            return redirect('feed_view')

    return render(request, 'Main/feed/feed_form.html')


def feed_view(request):
    posts = FeedPost.objects.all().order_by('-created_at')
    return render(request, 'Main/feed/feed_view.html', {'posts':posts})



@login_required
def delete_post(request, id):
    try:
        post = FeedPost.objects.get(id=id)
        
        # Check if the current user is the author of the post
        if post.author != request.user:
            raise PermissionDenied("You can only delete your own posts")
            
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('feed_view')
        
    except FeedPost.DoesNotExist:
        raise Http404("Post does not exist")

@login_required
def feed_edit(request, id):
    try:
        post = FeedPost.objects.get(id=id)
        
        # Check if the current user is the author of the post
        if post.author != request.user:
            raise PermissionDenied("You can only edit your own posts")
            
        if request.method == 'POST':
            caption = request.POST.get('caption')
            image = request.FILES.get('image')
            
            # Update fields
            post.caption = caption
            if image:
                post.image = image
            post.save()
            
            messages.success(request, 'Post updated successfully!')
            return redirect('feed_view')
            
        # GET request - show edit form
        return render(request, 'Main/feed/feed_edit.html', {'post': post})
        
    except FeedPost.DoesNotExist:
        raise Http404("Post does not exist")
    


@require_POST
@login_required
def toggle_like(request, post_id):
    post = FeedPost.objects.get(id=post_id)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)
        status = 'unliked'
    else:
        post.likes.add(user)
        status = 'liked'

    return JsonResponse({
        'status': status,
        'like_count': post.likes.count()
    })

def post_likes_view(request, post_id):
    post = get_object_or_404(FeedPost, id=post_id)
    liked_users = post.likes.all()
    return render(request, 'Main/feed/likes_feed.html', {'post': post, 'liked_users': liked_users})


def UnderConstruction_404(request):
    return render(request, 'Main/pages/UnderConstruction_404.html')
