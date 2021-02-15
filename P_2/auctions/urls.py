from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/", views.create, name = "create"),
    path("listing/<int:id>/", views.listing, name = "listing"),
    path("watchlist/", views.watchlist_view, name = "watchlist"),
    path("categories/", views.categories, name = "categories"),
    path("categories/<str:category>", views.category, name = "category")
]
urlpatterns += staticfiles_urlpatterns()