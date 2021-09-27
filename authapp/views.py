from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin

from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from basketapp.models import Basket
from authapp.models import User

# Create your views here.

class UserLoginView(LoginView):
    authentication_form = UserLoginForm
    template_name = 'authapp/login.html'
    extra_context = {
        'title': 'GeekShop - Авторизация',
        'form_class': 'col-lg-5',
        'header': 'Авторизация',
    }
    success_url = reverse_lazy('index')


# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user and user.is_active:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#     else:
#         form = UserLoginForm()
#     context = {
#         'form': form,
#         'title': 'GeekShop - Авторизация',
#         'form_class': 'col-lg-5',
#         'header': 'Авторизация',
#     }
#     return render(request, 'authapp/login.html', context)


class UserRegisterView(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'authapp/register.html'
    form_class = UserRegisterForm
    extra_context = {
        'title': 'GeekShop - Регистрация',
        'form_class': 'col-lg-7',
        'header': 'Создать аккаунт',
    }
    success_url = reverse_lazy('auth:login')
    success_message = 'Регистрация успешна!'
    


# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Регистрация успешна!')
#             return HttpResponseRedirect(reverse('auth:login'))
#     else:
#         form = UserRegisterForm()
#     context = {
#         'form': form,
#         'title': 'GeekShop - Регистрация',
#         'form_class': 'col-lg-7',
#         'header': 'Создать аккаунт',
#     }
#     return render(request, 'authapp/register.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


# class UserProfileView(UpdateView):
#     model = User
#     template_name = 'authapp/profile.html'
#     form_class = UserProfileForm
#
#     context = {
#         'title': 'GeekShop - Профиль',
#         'baskets': Basket.objects.filter(user=request.user),
#     }



@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Изменения сохранены')
            return HttpResponseRedirect(reverse('auth:profile'))
    else:
        form = UserProfileForm(instance=request.user)
    context = {
        'form': form,
        'title': 'GeekShop - Профиль',
        'baskets': Basket.objects.filter(user=request.user),
    }
    return render(request, 'authapp/profile.html', context)
