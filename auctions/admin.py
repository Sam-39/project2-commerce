from django.contrib import admin
from .models import User, Category, Listing, Comment, Bid

# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'active', 'seller')

class CommentAdmin(admin.ModelAdmin):
    list_display= ('user', 'listing', 'content')

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid)
