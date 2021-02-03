from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("entry/<str:title>/", views.entry, name = "entry"),
    path("search/", views.search, name = "search"),
    path("search_results/<str:searched>", views.search_results, name = "search_results"),
    path("create/", views.create_page, name = "create_page")
]
