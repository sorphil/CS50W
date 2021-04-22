from django.urls import path, include
from . import views


urlpatterns = [
                path('', views.index, name = "index"),
                path('<int:id>/', views.flight, name = "flight"),
                path('<int:id>/book/', views.book, name = 'book')
]