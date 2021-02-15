from django.urls import path, include
from . import views


urlpatterns = [
                path('', views.index, name = "index"),
                path('login/', views.login_view, name = "login_view"),
                path('logout/', views.logout_view, name = 'logout_view')
]