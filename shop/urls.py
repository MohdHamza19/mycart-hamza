from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="ShopHome"),
    path('about/', views.about, name="AboutUs"),
    path('contact/', views.contact, name="contact"),
    path('tracker/', views.tracker, name="TrackingStatus"),
    path('search/', views.search, name="Search"),
    path('login/', views.login, name="Login"),
    path('signup/', views.signup, name="Signup"),
    path('signout/', views.signout, name="Signout"),
    path('yourOrders/', views.yourOrders, name="YOurOrders"),
    path('products/<int:myid>', views.productView, name="ProductView"),
    path('checkout/', views.checkout, name="Checkout"),
    path('productbycategory/<str:cat>', views.category, name="Category"),
    path('review/<int:rid>', views.review, name="Review"),
]