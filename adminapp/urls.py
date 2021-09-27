from django.urls import path
# from adminapp.views import index, admin_users_read, admin_users_update, admin_users_create, admin_users_delete
from adminapp.views import index, UserListView, UserUpdateView, UserCreateView, UserDeleteView

app_name = 'adminapp'

urlpatterns = [
    path('', index, name='index'),
    path('users/', UserListView.as_view(), name='admin_users_read'),
    path('users-create/', UserCreateView.as_view(), name='admin_users_create'),
    path('users-update/<int:pk>', UserUpdateView.as_view(), name='admin_users_update'),
    path('users-delete/<int:pk>', UserDeleteView.as_view(), name='admin_users_delete'),
]
