from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('update_status_counts/', views.update_status_counts, name='update_status_counts'),
    path('login/', views.login, name='login'),
]
