from django.urls import path
from admindashboard import views

app_name = 'admindashboard'  

urlpatterns = [
    path('admin-dash-board/', views.index, name='dashboard'),
    path('users/', views.view_user, name='users'),
    path('user-details/<int:id>/', views.view_user_details, name='user-details'),
    path('list-product', views.list_product, name='list-product'),
    path('add-product', views.add_product, name='add-product'),
    path('delete-product/<int:id>/', views.delete_product, name='delete-product'),

    path('update/<int:id>/', views.edit_product, name='update'),
    path('update/<int:id>/', views.update_product, name='update-product'),
]