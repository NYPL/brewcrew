from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('google_callback/', views.google_callback, name='google_callback'),
]

