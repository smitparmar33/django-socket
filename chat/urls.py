from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
    path("user-status/<str:user_name>",views.UserStatusAPI.as_view(),name="user-status"),
]