from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings

from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from basketapp.models import Basket
from authapp.models import User

# Create your views here.


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


class UserLoginView(LoginView):
    authentication_form = UserLoginForm
    template_name = 'authapp/login.html'
    extra_context = {
        'title': 'GeekShop - Авторизация',
        'form_class': 'col-lg-5',
        'header': 'Авторизация',
    }


class UserRegisterView(CreateView):
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

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, **self.extra_context})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            if send_verify_mail(user):
                print('Сообщение для подтверждения регистрации отправлено')
                return HttpResponseRedirect(reverse('auth:login'))
            else:
                print('Ошибка отправки сообщения для подтверждения регистрации')
                return HttpResponseRedirect(reverse('auth:login'))
            # messages.success(request, self.success_message)
            # return HttpResponseRedirect(self.success_url)
        return render(request, self.template_name, {'form': form, **self.extra_context})


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


def send_verify_mail(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])
    title = f'Подтверждение учетной записи {user.username}'
    message = f'Для подтверждения учетной записи {user.username} на портале {settings.DOMAIN_NAME} перейдите по ' \
              f'ссылке: \n{settings.DOMAIN_NAME}{verify_link}'

    print(f'E-mail sent from: {settings.EMAIL_HOST_USER}, to: {user.email}')
    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activation_key):
    context = {
        'title': 'Подтверждение авторизации',
        'form_class': 'col-lg-5',
        'header': 'Поздравляем!',
    }

    try:
        user = User.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            print(f'User {user} is activated')
            user.is_active = True
            user.save()
            auth.login(request, user)
            return render(request, 'authapp/verification.html', context)
        else:
            print(f'Error activation user: {user}')
            return render(request, 'authapp/verification.html', context)
    except Exception as e:
        print(f'Error activation user: {e.args}')
    return HttpResponseRedirect(reverse('index'))

