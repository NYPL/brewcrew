from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('prepopulate', views.prepopulate, name='prepopulate'),
    path('sasb_users', views.sasb_users, name='sasb_users'),
    path('find_coffee_match', views.find_coffee_match, name='find_coffee_match'),

]

