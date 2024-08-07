from django.urls import path
from authuser import views
from django.contrib.auth import views as auth_views

app_name = 'auth'  

urlpatterns = [
    path('sign_in/', views.register_view, name='sign_in'),
    path('log_in/', views.login_user, name='login'),
    path('log_out/', views.user_logout, name='logout'),
    path('forget-password/', views.forget_password, name='forget_password'),

    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

