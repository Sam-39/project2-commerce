from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listings/<int:listing_id>", views.listing, name="listing"),
    path("categories/", views.categories, name="categories"),
    path("categories/<str:listing_cat>", views.category, name="category"),
    path("close/<int:listing_id>", views.close, name="close"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/add/<int:listing_id>", views.watchlist_add, name="watchlist_add"),
    path("watchlist/remove/<int:listing_id>", views.watchlist_remove, name="watchlist_remove"),
]
