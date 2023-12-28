from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Post, User, Episode, Favorite, WatchHistory
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from .forms import MyLoginForm, UserRegistrationForm , PostAddForm, PostEditForm, EpisodeAddForm, EpisodeEditForm # Import your form here
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.
@login_required
def posts_list(request):
    user = request.user
    search_term = request.GET.get('searchpost')
    if search_term:
        # if there is a valid search term ,filter the list of objects with it
        posts_list = Post.objects.filter(author=user,title__icontains = search_term)

    else:
        posts_list = Post.objects.filter(author=user)


    # Check if the user belongs to the 'content_creators' group
    is_subscriber = user.groups.filter(name='subscribers').exists()
    is_content_creators = user.groups.filter(name='content_creators').exists()
    # posts_list = Post.objects.all()

    # posts_list = Post.objects.filter()


    context = {
        'posts_list': posts_list,

    }
    return render(request, 'posts.html',{'search_term': search_term,'posts_list': posts_list,'is_subscriber': is_subscriber, 'is_content_creators': is_content_creators})

def home(request):
    return render(request, 'index.html', {'home': home})

def adminpage(request):
    return render(request, 'adminpage.html',{'adminpage': adminpage})


def creatorposts(request):
    user = request.user

    # Check if the user belongs to the 'content_creators' group
    is_subscriber = user.groups.filter(name='subscribers').exists()
    is_content_creators = user.groups.filter(name='content_creators').exists()

    # return render(request, 'topbar.html', {'is_subscriber': is_subscriber, 'is_content_creators': is_content_creators})

    return render(request, 'creatorposts.html',{'creatorposts': creatorposts,'is_subscriber': is_subscriber, 'is_content_creators': is_content_creators})

def subscriber(request):
    user = request.user

    # Check if the user belongs to the 'content_creators' group
    is_subscriber = user.groups.filter(name='subscribers').exists()
    is_content_creators = user.groups.filter(name='content_creators').exists()
    movies = Post.objects.filter(movie_media_genre__title = 'Movie')
    series = Post.objects.filter(movie_media_genre__title = 'Series')
    tvshows = Post.objects.filter(movie_media_genre__title = 'TV shows')
    originals = Post.objects.filter(movie_media_genre__title = 'Originals')

    return render(request, 'subscriber.html',{'subscriber': subscriber,'is_subscriber': is_subscriber, 'is_content_creators': is_content_creators,'movies': movies,'series': series,'tvshows': tvshows,'originals': originals})

def user_login_view(request):
    if request.method == 'POST':
        login_form = MyLoginForm(request.POST)

        if login_form.is_valid():
            cleaned_data = login_form.cleaned_data
            auth_user = authenticate(
                request,
                username=cleaned_data['username'],
                password=cleaned_data['password']
            )

            if auth_user is not None:
                login(request, auth_user)
                # Redirect to a different page upon successful login
                if request.user.is_superuser:
                    redirect_url = '/adminpage/'
                elif request.user.groups.filter(name='content_creators').exists():
                    redirect_url = '/creatorposts/'
                elif request.user.groups.filter(name='subscribers').exists():
                    redirect_url = '/subscriber/'
                else:
                    redirect_url = '/home/'
                return HttpResponseRedirect(redirect_url)
            else:
                # return HttpResponse('<h1>NOT Authenticated</h1>')
                return redirect('home')

    else:
        login_form = MyLoginForm()

    return render(request, 'useraccount/userlogin.html', {'login_form': login_form})




def register(request):
    user = request.user

    # Check if the user belongs to the 'content_creators' group
    is_subscriber = user.groups.filter(name='subscribers').exists()
    is_content_creators = user.groups.filter(name='content_creators').exists()

    if request.method == 'POST':
        user_reg_form = UserRegistrationForm(request.POST)
        if user_reg_form.is_valid():
            new_user = user_reg_form.save(commit=False)
            new_user.set_password(user_reg_form.cleaned_data['password'])
            new_user.save()

            group = Group.objects.get(name='subscribers')
            new_user.groups.add(group)
            return render(request, 'account/register_done.html',{'user_reg_form': user_reg_form,'is_subscriber': is_subscriber, 'is_content_creators': is_content_creators})

    else:
        user_reg_form = UserRegistrationForm()

    return render(request, 'account/register.html', {'user_reg_form': user_reg_form,'is_subscriber': is_subscriber, 'is_content_creators': is_content_creators})


def registercreator(request):
    user = request.user

    # Check if the user belongs to the 'content_creators' group
    is_subscriber = user.groups.filter(name='subscribers').exists()
    is_content_creators = user.groups.filter(name='content_creators').exists()
    if request.method == 'POST':
        user_reg_form = UserRegistrationForm(request.POST)
        if user_reg_form.is_valid():
            new_user = user_reg_form.save(commit=False)
            new_user.set_password(user_reg_form.cleaned_data['password'])
            new_user.save()

            group = Group.objects.get(name='content_creators')
            new_user.groups.add(group)
            return render(request, 'account/register_done.html',{'user_reg_form': user_reg_form,'is_subscriber': is_subscriber, 'is_content_creators': is_content_creators})

    else:
        user_reg_form = UserRegistrationForm()

    return render(request, 'account/registercreator.html', {'user_reg_form': user_reg_form,'is_subscriber': is_subscriber, 'is_content_creators': is_content_creators})

@login_required
def add_post(request):
    user = request.user

    # Check if the user belongs to the 'content_creators' group
    is_subscriber = user.groups.filter(name='subscribers').exists()
    is_content_creators = user.groups.filter(name='content_creators').exists()
    add_post_form = PostAddForm(request.POST,request.FILES)
    if request.method == 'POST':
        if add_post_form.is_valid():
            post = add_post_form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('creatorposts')
    else:
        add_post_form = PostAddForm()

    return render(request, 'account/add_post.html',{'add_post_form': add_post_form,'is_subscriber': is_subscriber, 'is_content_creators': is_content_creators})
@login_required
def edit_post(request,passed_id):
    post_details = get_object_or_404(Post, id=passed_id)
    edit_post_form = PostEditForm(request.POST or None,request.FILES or None, instance=post_details)
    user = request.user

    # Check if the user belongs to the 'content_creators' group
    is_subscriber = user.groups.filter(name='subscribers').exists()
    is_content_creators = user.groups.filter(name='content_creators').exists()

    if edit_post_form.is_valid():
        edit_post_form.save()
        return redirect('creatorposts')

    return render(request, 'account/edit_post.html', {'edit_post_form': edit_post_form, 'is_subscriber': is_subscriber, 'is_content_creators': is_content_creators})

@login_required
def delete_post(request, passed_id):
    post_details = get_object_or_404(Post, id=passed_id)
    post_details.delete()
    return redirect('creatorposts')

def toggle_user_status(request, user_id):
    if request.user.is_superuser:
        user = get_object_or_404(User, id=user_id)
        user.is_active = not user.is_active
        user.save()
        messages.success(request, f"User {user.username}'s status has been updated.")
    else:
        messages.error(request, "You do not have permission to perform this action.")

    return redirect('user_list')


def user_list(request):
    # Get the 'content_creators' and 'subscribers' groups
    content_creators_group = Group.objects.get(name='content_creators')
    subscribers_group = Group.objects.get(name='subscribers')

    # Filter users based on group membership
    content_creators = content_creators_group.user_set.all()
    subscribers = subscribers_group.user_set.all()

    return render(request, 'user_list.html', {'content_creators': content_creators, 'subscribers': subscribers})



def post_details_view(request,passed_id):
    post_details = get_object_or_404(Post, id=passed_id)
    episode_details = Episode.objects.filter(post__in=[passed_id])
    user = request.user

    # Check if the user belongs to the 'content_creators' group
    is_subscriber = user.groups.filter(name='subscribers').exists()
    is_content_creators = user.groups.filter(name='content_creators').exists()


    return render(request, 'postdetails.html',{'post_details': post_details ,'episode_details': episode_details,'is_subscriber': is_subscriber, 'is_content_creators': is_content_creators})

@login_required
def your_view(request):
    # Your view logic here
    user = request.user

    # Check if the user belongs to the 'content_creators' group
    is_subscriber = user.groups.filter(name='subscribers').exists()
    is_content_creators = user.groups.filter(name='content_creators').exists()

    return render(request, 'topbar.html',{'is_subscriber': is_subscriber, 'is_content_creators': is_content_creators })

@login_required
def add_episode(request, passed_id):
    user = request.user

    # Check if the user belongs to the 'content_creators' group
    is_subscriber = user.groups.filter(name='subscribers').exists()
    is_content_creators = user.groups.filter(name='content_creators').exists()
    add_episode_form = EpisodeAddForm(request.POST)
    if request.method == 'POST':
        if add_episode_form.is_valid():
            review = add_episode_form.save(commit=False)
            review.author = request.user
            review.post_id = passed_id
            review.save()
            return redirect('detail_path', passed_id)
        else:
            add_episode_form = EpisodeAddForm()
    return render(request, 'account/add_episode.html', {'add_episode_form': add_episode_form,'is_subscriber': is_subscriber, 'is_content_creators': is_content_creators})

@login_required
def edit_episode(request,passed_id):
    user = request.user

    # Check if the user belongs to the 'content_creators' group
    is_subscriber = user.groups.filter(name='subscribers').exists()
    is_content_creators = user.groups.filter(name='content_creators').exists()

    episode_details = get_object_or_404(Episode, id=passed_id)
    edit_episode_form = EpisodeEditForm(request.POST or None,request.FILES or None, instance=episode_details)

    if edit_episode_form.is_valid():
        edit_episode_form.save()
        return redirect('subscriber_list')

    return render(request, 'account/edit_episode.html', {'edit_episode_form': edit_episode_form ,'episode_details': episode_details,'is_subscriber': is_subscriber, 'is_content_creators': is_content_creators})

@login_required
def delete_episode(request, passed_id):
    post_details = get_object_or_404(Episode, id=passed_id)
    post_details.delete()
    return redirect('creatorposts')



@login_required
def subscriber_list(request):

    user = request.user

    # Check if the user belongs to the 'content_creators' group
    is_subscriber = user.groups.filter(name='subscribers').exists()
    is_content_creators = user.groups.filter(name='content_creators').exists()

    search_term = request.GET.get('searchpost')
    # if search_term:
    #     # if there is a valid search term ,filter the list of objects with it
    #     posts_list = Post.objects.filter(author=user, title__icontains=search_term)
    #
    # else:
    #     posts_list = Post.objects.filter(author=user)
    movies = Post.objects.filter(movie_media_genre__title = 'Movie')
    series = Post.objects.filter(movie_media_genre__title = 'Series')
    tvshows = Post.objects.filter(movie_media_genre__title = 'TV shows')
    originals = Post.objects.filter(movie_media_genre__title = 'Originals')

    return render(request, 'subscriber.html', {'movies': movies,'series': series,'tvshows': tvshows,'originals': originals,'is_subscriber': is_subscriber, 'is_content_creators': is_content_creators})

@login_required
def admin_list(request):
    user = request.user

    # Check if the user belongs to the 'content_creators' group
    is_subscriber = user.groups.filter(name='subscribers').exists()
    is_content_creators = user.groups.filter(name='content_creators').exists()
    movies = Post.objects.filter(movie_media_genre__title = 'Movie')
    series = Post.objects.filter(movie_media_genre__title = 'Series')
    tvshows = Post.objects.filter(movie_media_genre__title = 'TV shows')
    originals = Post.objects.filter(movie_media_genre__title = 'Originals')

    return render(request, 'admin_posts.html',
                  {'movies': movies, 'series': series, 'tvshows': tvshows, 'originals': originals,'is_subscriber': is_subscriber, 'is_content_creators': is_content_creators})



def toggle_favorite_view(request, post_id):

    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if user in post.favorited_by.all():
        # Remove from favorites
        post.favorited_by.remove(user)
    else:
        # Add to favorites
        post.favorited_by.add(user)

    return redirect('detail_path', passed_id=post_id)

def favorite_list_view(request):
    user = request.user

    # Check if the user belongs to the 'content_creators' group
    is_subscriber = user.groups.filter(name='subscribers').exists()
    is_content_creators = user.groups.filter(name='content_creators').exists()

    favorites = user.favorite_posts.all()

    return render(request, 'favorites.html', {'favorites': favorites,'is_subscriber': is_subscriber, 'is_content_creators': is_content_creators})






# @login_required
# def add_to_watch_history(request):
#     if request.method == 'POST':
#         movie_id = request.POST.get('id')
#         movie = get_object_or_404(Post, id=movie_id)  # Replace ContentModel with your actual model
#         user = request.user
#
#         # Check if the user has already watched this content
#         if not WatchHistory.objects.filter(user=user, content=movie).exists():
#             WatchHistory.objects.create(user=user, content=movie)
#
#         return JsonResponse({'message': 'Movie added to watch history'})
#
#     return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def add_to_watch_history(request, content_id):
    if request.method == 'POST':
        movie = get_object_or_404(Post, id=content_id)  # Replace ContentModel with your actual model
        user = request.user

        # Check if the user has already watched this content
        if not WatchHistory.objects.filter(user=user, content=movie).exists():
            WatchHistory.objects.create(user=user, content=movie)

        # Redirect to the page where the user clicked the movie
        return redirect('detail_path', passed_id=content_id)

    # Handle the case where it's not a POST request (optional)
    return HttpResponseBadRequest("Invalid request")



# @login_required
# def watch_history(request):
#     user = request.user
#     watch_history = WatchHistory.objects.filter(user=user).order_by('-timestamp')
#
#     context = {
#         'watch_history': watch_history,
#     }
#
#     return render(request, 'watch_history.html', context)

from .models import WatchHistory

@login_required
def watch_history(request):
    user = request.user


    # Check if the user belongs to the 'content_creators' group
    is_subscriber = user.groups.filter(name='subscribers').exists()
    is_content_creators = user.groups.filter(name='content_creators').exists()
    watch_history = WatchHistory.objects.filter(user=user).order_by('-timestamp')

    context = {
        'watch_history': watch_history,
    }

    return render(request, 'watch_history.html', {'watch_history': watch_history,'is_subscriber': is_subscriber, 'is_content_creators': is_content_creators})
