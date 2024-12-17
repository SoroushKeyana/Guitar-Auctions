from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create_listing"),
    path("categories/", views.categories_page, name="categories_page"),
    path("category/<str:category_name>/", views.category, name="category"),    
    path("listing/<int:id>", views.listing, name="listing"),
    path("addWatchlist/<int:id>", views.add_watchlist, name="add_watchlist"),
    path("removeWatchlist/<int:id>", views.remove_watchlist, name="remove_watchlist"),
    path("watchlist", views.display_watchlist, name="watchlist"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("bid/<int:id>", views.bid, name="bid"),
    path("endAuction/<int:id>", views.end_auction, name="end_auction"),
    path("my_listings", views.my_listings, name="my_listings"),
]
