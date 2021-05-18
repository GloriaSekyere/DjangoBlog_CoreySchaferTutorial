from django.urls import path 
from django.contrib.auth import views as auth_views
from . import views


app_name = 'users'

urlpatterns = [

    path('register/', views.register, name='register'),
    
    path('login/', 
        auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    
    path('logout/', 
        auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    
    path('profile/', views.profile, name='profile'),

    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),

    # Password reset request sent to email
    path('password_reset_done/', 
        auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), 
        name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>/', views.PasswordConfirm.as_view(), name='password_reset_confirm'),

    path('password_reset_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), 
        name='password_reset_complete'),
]

# template_name='users/password_reset.html'
# auth_views.PasswordResetDoneView.as_view(), template_name='users/password_reset_done.html'
# template_name='users/password_reset_confirm.html'