from django.contrib import admin
from .models import *
class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "start_bid", "category", "user", "pub_date")
    filter_horizontal = ("watchers", "watchers")
    
# class BidAdmin(admin.ModelAdmin):
#     list_display = ("bidder", "amount", "item")
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "listing")
# Register your models here.
admin.site.register(User)
admin.site.register(AuctionListing, AuctionListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment, CommentAdmin)