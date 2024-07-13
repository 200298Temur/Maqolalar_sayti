from django.urls import path
from .views import *

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("addpage/", AddPage.as_view(), name='add_page'),
    path('category/<slug:cat_slug>/', CategoryView.as_view(), name='category'),
   
    path('post/<slug:post_slug>/', show_post, name='post'),
    path('post_update/<slug:post_update_slug>/', show_post_update, name='post_update'),
    path('about/', About.as_view(), name='about'),

    path('muharir/', MuharrirKabinet.as_view(), name='muharir'),
    path('author/<slug:author_id>/', AuthorView.as_view(), name='author'),
    path('author_main/<slug:author_id>/', AuthorViewMain.as_view(), name='author_main'),

    path('no-permission/', no_permission_view, name='no_permission'),
    path('update/<slug:slug>/', UpdatePage.as_view(), name='update'),
]
