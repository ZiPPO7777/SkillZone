from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views 

urlpatterns = [
    path('UnderConstruction_404', views.UnderConstruction_404, name='UnderConstruction_404'),
    path('', views.public_homepage, name='welcome'),
    path('home/', views.home, name='home'),
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('about/', views.about, name='about'),
    path('feed_post/', views.feed_post, name='feed_post'),
    path('feed_view/', views.feed_view, name='feed_view'),
    path('feed/<int:id>/edit/', views.feed_edit, name='feed_edit'),
    path('feed/<int:id>/delete/', views.delete_post, name='delete_post'),

    path('toggle-like/<int:post_id>/', views.toggle_like, name='toggle_like'),
    path('post/<int:post_id>/likes/', views.post_likes_view, name='post_likes'),
    
   
    #



    



] 
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
