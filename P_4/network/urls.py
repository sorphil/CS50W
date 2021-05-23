
from django.urls import path
from . import views




urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:user_name>", views.profile_index, name = "profile_index"),
    path("following", views.following_index, name = "following"),
    # API Routes
    path("posts", views.load_posts_index, name="load_posts"),
    # path("posts/<int:page_no>", views.paginator, name = "paginate"),
    path("following/load", views.following_load, name = "load_following_posts"),
    path("posts/<int:post_id>", views.likepost, name="userpost_like"),
    path("profile_load/<str:user_name>", views.profile_load, name = "load_profile"),
    path("follow_unfollow/<str:user_name>", views.follow_unfollow, name = "follow/unfollow"),
    path("edit/<int:post_id>", views.edit_post, name = "edit")
]


