from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from authapp.models import User
from adminapp.forms import UserAdminRegistrationForm, UserAdminProfileForm

# Create your views here.


@user_passes_test(lambda x: x.is_superuser)
def index(request):
    return render(request, 'adminapp/index.html')


# READ
class UserListView(ListView):
    model = User
    template_name = 'adminapp/admin-users-read.html'

    @method_decorator(user_passes_test(lambda x: x.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserListView, self).dispatch(request, *args, **kwargs)

# @user_passes_test(lambda x: x.is_superuser)
# def admin_users_read(request):
#     context = {
#         'users': User.objects.all()
#     }
#     return render(request, 'adminapp/admin-users-read.html', context)


# CREATE
class UserCreateView(CreateView):
    model = User
    template_name = 'adminapp/admin-users-create.html'
    form_class = UserAdminRegistrationForm
    success_url = reverse_lazy('admin_staff:admin_users_read')

# @user_passes_test(lambda x: x.is_superuser)
# def admin_users_create(request):
#     if request.method == 'POST':
#         form = UserAdminRegistrationForm(data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admin_staff:admin_users_read'))
#     else:
#         form = UserAdminRegistrationForm()
#     context = {
#         'form': form,
#         'title': 'GeekShop - Регистрация',
#         'form_class': 'col-lg-7',
#         'header': 'Создание пользователя',
#     }
#     return render(request, 'adminapp/admin-users-create.html', context)


# UPDATE
class UserUpdateView(UpdateView):
    model = User
    template_name = 'adminapp/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admin_staff:admin_users_read')


# @user_passes_test(lambda x: x.is_superuser)
# def admin_users_update(request, user_id):
#     user = User.objects.get(id=user_id)
#     if request.method == 'POST':
#         form = UserAdminProfileForm(data=request.POST, instance=user, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admin_staff:admin_users_read'))
#     else:
#         form = UserAdminProfileForm(instance=user)
#     context = {
#         'form': form,
#         'user': user,
#     }
#     return render(request, 'adminapp/admin-users-update-delete.html', context)


# DELETE
class UserDeleteView(DeleteView):
    model = User
    template_name = 'adminapp/admin-users-update-delete.html'
    success_url = reverse_lazy('admin_staff:admin_users_read')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

# @user_passes_test(lambda x: x.is_superuser)
# def admin_users_delete(request, user_id):
#     user = User.objects.get(id=user_id)
#     user.is_active = False
#     user.save()
#     return HttpResponseRedirect(reverse('admin_staff:admin_users_read'))

