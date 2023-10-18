from django.urls import path
from authuser import views

app_name = 'auth'  

urlpatterns = [
    path('sign_in/', views.register_view, name='sign_in'),
    path('log_in/', views.login_user, name='login'),
    path('log_out/', views.user_logout, name='logout'),
]