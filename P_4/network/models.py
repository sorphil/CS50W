from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields.related import OneToOneField, RelatedField
from datetime import datetime
from django.db.models.deletion import CASCADE



class User(AbstractUser):
    pass

class UserPost(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=CASCADE, related_name="user_post")
    pub_date = models.DateTimeField(default=datetime.now(), editable=False)
    likes = models.ManyToManyField(User, blank=True,  related_name="likes")
        
    def __str__(self):
        return f"Post #{self.pk} by {self.user}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE, related_name="user_profile")
    followers = models.ManyToManyField(User, blank = True, related_name="follower_user")
    following = models.ManyToManyField(User, blank=True, related_name="following_user") 

    def __str__(self):
        return f"{self.user}'s profile"