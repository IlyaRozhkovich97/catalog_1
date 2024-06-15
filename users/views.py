import random
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from config import settings
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User
CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-*!&$#?=@'


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        token = ''
        for i in range(10):
            token += random.choice(CHARS)
        form.verified_pass = token
        user = form.save()
        user.token = token
        send_mail(
            subject='Верификация почты',
            message=f'Поздравляем с регистрацией на SkyStore \n'
                    f'Для подтверждения регистрации перейдите по ссылке: \n'
                    f'http://127.0.0.1:8000/users/confirm/{user.token} \n'
                    f'Если вы не причастны к регистрации игнорируйте это письмо.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def verify_view(request, token):
    user = User.objects.get(token=token)
    user.is_verified = True
    user.save()
    return render(request, 'users/verify.html')


def res_password(request):
    new_password = ''
    if request.method == 'POST':
        email = request.POST['email']
        user = get_object_or_404(User, email=email)
        for i in range(10):
            new_password += random.choice(CHARS)
        send_mail(
            subject='Смена пароля',
            message=f'Ваш новый пароль {new_password}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )
        user.set_password(new_password)
        user.save()
        return redirect(reverse('users:login'))
    return render(request, 'users/reset_password.html')


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
