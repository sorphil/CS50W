from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

CATEGORY_CHOICES = [
    ('Fashion', "Fashion"),
    ('Automotive', 'Automotive'),
    ('Toys, Games & Baby', "Toys, Games & Baby"),
    ('Health, Beauty & Perfumes', "Health, Beauty & Perfumes"),
    ('Electronics', "Electronics"),
    ('Home, Kitchen & Pets', 'Home, Kitchen & Pets'),
    ('Books & Office Supplies', "Books & Office Supplies"),
    ('Food & Groceries', "Food & Groceries"),
    ('Sports, Fitness & Outdoors', 'Sports, Fitness & Outdoors'),
    ('Tools & Home Improvement', "Tools & Home Improvement"),
    ('Other', "Other")
]

class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_bid = models.PositiveIntegerField()
    category =models.CharField(choices=sorted(CATEGORY_CHOICES), max_length=40)
    image = models.ImageField( upload_to=user_directory_path)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing")
    pub_date = models.DateTimeField(default = now, editable= False)
    active = models.BooleanField()
    cur_price = models.PositiveIntegerField(blank = True, null= True)
    watchers = models.ManyToManyField(User, blank=True, related_name="watchers")
    def __str__(self):
        return f"{self.title}({self.category}) - Starting bid of ${self.start_bid}"



class Bid(models.Model):
    amount = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user} bids {self.amount} on {self.listing}" 
    
    


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    text = models.TextField(default="")
    def __str__(self):
        return f"Comment by {self.user} on {self.listing}" 