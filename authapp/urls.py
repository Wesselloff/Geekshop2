from django.urls import path, re_path
# from authapp.views import login, register, logout, profile
from authapp.views import UserLoginView, UserRegisterView, logout, profile, verify

app_name = 'authapp'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    # path('login/', login, name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    # path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
    re_path(r'^verify/(?P<email>.+)/(?P<activation_key>\w+)/$', verify, name='verify'),
]
