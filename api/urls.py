from django.urls import path
from . import views


urlpatterns = [
    path('', views.fetch_data, name='index'),
    path('login/', views.login, name='login'),
]
