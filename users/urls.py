from django.urls import include, path
from allauth.account.views import signup
from .views import *

app_name = 'users'
urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register_signup/', RegisterUser.as_view(), name='register_signup'),
    path('profile/', ProfileUser.as_view(), name='profile'),
    path('maqolam/', Kabinet.as_view(), name='maqolam'),
]