from django.urls import path

from . import views

urlpatterns = [
    path('', views.status, name='status'),
    path('status', views.status, name='status'),
    path('enable', views.enable, name='enable')
]