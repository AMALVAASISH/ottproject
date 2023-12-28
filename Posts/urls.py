from django.urls import path
from .views import posts_list, user_login_view, home, register, creatorposts, subscriber, toggle_user_status, user_list
from .views import post_details_view, registercreator, add_post, edit_post, delete_post, add_episode, adminpage, admin_list, subscriber_list, toggle_favorite_view
from django.contrib.auth.views import LogoutView
from .views import favorite_list_view, delete_episode
from .views import edit_episode, add_to_watch_history, watch_history
urlpatterns = [
    path('', home,name='home'),
    path('post/<int:passed_id>/', post_details_view,name='detail_path'),
    path('adminpage/', adminpage, name='adminpage'),
    path('creatorposts/',creatorposts,name='creatorposts'),
    # path('subscriber/', subscriber, name='subscriber'),
    path('creator/', posts_list, name='creator'),
    path('login/', user_login_view, name='login'),
    path('logout/',LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('registercreator/', registercreator, name='registercreator'),
    path('toggle_user_status/<int:user_id>/', toggle_user_status, name='toggle_user_status'),
    path('user_list/', user_list, name='user_list'),
    path('account/add_post/', add_post, name='add_post'),
    path('account/edit_post/<int:passed_id>/',edit_post, name='edit_post'),
    path('account/delete_post/<int:passed_id>/',delete_post, name='delete_post'),
    path('account/add_episode/<int:passed_id>/', add_episode, name='add_episode'),
    path('account/edit_episode/<int:passed_id>/', edit_episode, name='edit_episode'),
    path('account/delete_episode/', delete_episode, name='delete_episode'),
    path('admin_posts/', admin_list, name='admin_posts'),
    path('subscriber/', subscriber_list, name='subscriber_list'),
    path('toggle_favorite/<int:post_id>/', toggle_favorite_view, name='toggle_favorite'),
    path('favorites/', favorite_list_view, name='favorite_list'),
    path('add_to_watch_history/<int:content_id>/', add_to_watch_history, name='add_to_watch_history'),
    path('watch_history/', watch_history, name='watch_history'),





]

