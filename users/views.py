from django.http import HttpResponseRedirect, HttpResponse

from django.shortcuts import render, reverse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from users.forms import UserRegisterForm, UserLoginForm, UserForm, UserUpdateForm
from users.models import User

def user_register_view(request):
    form = UserRegisterForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            new_user = form.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return HttpResponseRedirect(reverse('users:login_user'))
    context = {
        'form': form
    }
    return render(request, 'users/register_user.html', context)


def user_login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(email=cd['email'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('dogs:index'))
                else:
                    return HttpResponse('Аккаунт неактивен!')
    else:
        form = UserLoginForm()
    context = {
        'form': form
    }
    return render(request, 'users/login_user.html', context)


@login_required
def user_profile_view(request):
    user_object = request.user
    context = {
        'title': f'Ваш профиль {user_object.first_name}',
    }
    return render(request, 'users/user_profile.html', context)

@login_required
def user_update_view(request):
    user_object = request.user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user_object)
        if form.is_valid():
            user_object = form.save()
            user_object.save()
            return HttpResponseRedirect(reverse('users:profile_user'))
    user_name = user_object.first_name
    context = {
        'user_object': user_object,
        'title': f'Изменить профиль {user_name}',
        'form': UserUpdateForm,
    }
    return render(request, 'users/update_user.html', context)

def user_logout_view(request):
    logout(request)
    return redirect('dogs:index')
