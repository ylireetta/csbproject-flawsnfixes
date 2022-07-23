from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('allmoves/', views.allmovesView, name='allmoves'),
    path('addmove/', views.addmoveView, name='addmove'),
    path('searchsessions/', views.searchSessionsView, name='searchsessions'),
    path('addsession/', views.addSessionView, name='addsession'),
]