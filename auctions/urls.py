from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("auction/<str:id>", views.auction, name="auction"),
    path("toggle_watchlist/<str:listing_id>", views.toggle_watchlist, name="toggle_watchlist"),
    path("close/<str:listing_id>", views.close, name="close"),
    path('add_comment/<int:listing_id>', views.add_comment, name='add_comment'), 
    path('watchlist', views.watchlist, name='watchlist'), 
    path('categories/', views.categories, name='categories'),
    path('category/<int:category_id>/', views.category_listings, name='category_listings'),
]
 