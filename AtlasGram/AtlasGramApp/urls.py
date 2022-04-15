from django.urls import path
from . import views
from .views import PostListView,PostDetailView,PostCreateView,PostUpdateView,PostDeleteView, UserPostListView,CommentDeleteView,LikeView

urlpatterns = [
    path('', PostListView.as_view(), name = 'home'),
    path('user/<str:username>', UserPostListView.as_view(), name = 'user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name = 'post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name = 'post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name = 'post-delete'),
    path('postcomment/<int:pk>/delete/', CommentDeleteView.as_view(), name='postcomment-delete'),

    path('like/<int:pk>', LikeView, name='like_post'),

    path('news/', views.news, name='news'),
    path('about/', views.about, name = 'about'),
    path('calendar/', views.calendar, name = 'calendar'),
    path('contacts/', views.contacts, name = 'contact')
]