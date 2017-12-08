from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.index, name='index'),
    path('google_callback', views.google_callback, name='google_callback'),
    path('register/', views.register, name='register'),
]

