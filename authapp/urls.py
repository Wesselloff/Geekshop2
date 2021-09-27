from django.urls import path
# from authapp.views import login, register, logout, profile
from authapp.views import UserLoginView, UserRegisterView, logout, profile
# from authapp.views import UserLoginView, register, logout, profile

app_name = 'authapp'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    # path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
]
