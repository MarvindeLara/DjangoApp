from django.urls import path

from . import views

app_name = 'youtube'
urlpatterns = [
    path('', views.index, name='index'),
    path('results', views.search_results, name='search_results'),
    path('video/view/<int:pk>', views.video_view, name='video_view'),
    path('video/view/like/<int:pk>', views.video_like, name='video_like'),
    path('video/myvideos', views.video_myvideos, name='video_myvideos'),
    path('video/new', views.video_new, name='video_new'),
    path('video/view/addtoplaylist/<int:pk>', views.video_addtoplaylist, name='video_addtoplaylist'),
    path('addtoplaylist/<int:pk>', views.video_addtoplaylist_fromindex, name='video_addtoplaylist_fromindex'),
    path('video/myplaylist', views.video_myplaylist, name='video_myplaylist'),
    path('video/deletefromplaylist/<int:pk>', views.video_deletefromplaylist, name='video_deletefromplaylist'),
    path('video/edit/<int:pk>', views.video_edit, name='video_edit'),
    path('video/delete/<int:pk>', views.video_delete, name='video_delete'),
]