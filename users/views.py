from django.shortcuts import render, redirect
from .forms import UserRegistrationFrom, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy



def register(request):

    if request.method != "POST":
        form = UserRegistrationFrom()
    else:
        form = UserRegistrationFrom(data=request.POST)
        if form.is_valid():
            newuser = form.save()
            login(request, newuser)
            username = form.cleaned_data.get('username')
            messages.success(request, "Your account has been created.")
            return redirect('blog:blog-index')
    context = {'form':form}
    return render(request, 'users/register.html', context)

@login_required
def profile(request):
    if request.method != "POST":
        user_update_form = UserUpdateForm(instance=request.user)
        profile_update_form = ProfileUpdateForm(instance=request.user.profile)
    else:  
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_update_form = ProfileUpdateForm(request.POST, request.FILES, 
                                                instance=request.user.profile)
        if user_update_form.is_valid and profile_update_form.is_valid:
            user_update_form.save()
            profile_update_form.save()
            messages.success(request, "Your account has been updated.")
            return redirect('users:profile')
    
    context = {'user_update_form':user_update_form,
               'profile_update_form':profile_update_form,}
    return render(request, 'users/profile.html', context)


class PasswordReset(PasswordResetView):
    email_template_name = 'users/password_reset_email.html'
    template_name='users/password_reset.html'
    success_url = reverse_lazy('users:password_reset_done')

class PasswordConfirm(PasswordResetConfirmView):
    template_name='users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')