from django.urls import path
from .views import admin_home, users_list, broadcast_view

urlpatterns = [
    path('admin/', admin_home, name='admin_home'),
    path('admin/clients/', users_list, name='users_list'),
    path('admin/broadcast/', broadcast_view, name='broadcast'),
]
