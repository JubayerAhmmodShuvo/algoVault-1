from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('about', views.About_Us, name='aboutUs'),
    path('profile', views.User_Profile, name='profile'),
    path('updateprofile', views.Update_Profile, name='updateprofile'),
    path('contact', views.Contact_Us, name='contactUs'),
    path('tutorials', views.tutorial_list, name='tutorials'),
    path('details/<tut_id>', views.tutorial_details, name='tutDetails'),
    path('marked/<tut_id>', views.mark_as_done, name='markdone'),
    path('approved', views.approved_posts, name='approvedposts'),
    path('pending', views.pending_posts, name='pendingposts'),
    path('review', views.review_posts, name='reviewposts'),
    path('approve/<post_id>', views.approve_post, name='approve'),
    path('addtutorial', views.add_tutorial, name='addtutorial'),
    path('view/<post_id>', views.view_post, name='viewpost'),
    path('edit/<post_id>', views.edit_post, name='editpost'),
    path('progress', views.progress_view, name='progress')
]