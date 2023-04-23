from django.urls import path
from . import views


urlpatterns = [
    # login
    path('', views.login, name="login_Page"),
    path('login_handle/', views.login_handle, name="login_handle"),

    path('sign_up/', views.signup, name="sign_Page"),
    path('signup_handle/', views.signup_handle, name="signPage_handle"),

    # signOut
     path('sign_out/', views.signout, name="sign_out"),

    # product urls
    path('home/', views.home, name="Home Page"),
    path('store/',views.store, name="all_store"),
    path('hot-deals/',views.hotDeals, name="hot deals"),
    path('search_product/',views.search_products, name="search-product"),
    path('collections/<str:slug>/',views.collections_view, name="collections_view"),

    # add to cart
    path('add_to_cart/',views.add_to_cart, name="add_to_cart"),
    path('add_to_cart_home/',views.add_to_cart_home, name="add_to_cart_home"),
    path('removeCart/<int:id>',views.removeCart, name="removeCart"),

    # add to wishlish
    path('add_to_wishlist/',views.add_to_wishlist, name="add_to_wishlist"),
    path('removeWishlist/<int:id>',views.removeWishlist, name="removeWishlist"),

    path('About/', views.about_Us, name="About Page"),

    path('Contact/', views.contact, name="Contact Page"),
    path('add_new_contact/', views.add_new_cont, name="new contact"),


    path('Tracker/', views.tracker, name="Tracker Page"),
    path('product/<int:id>', views.product_view, name="View Page"),
    path('checkout/', views.checkout, name="CheckOut_Page"),
    path('order_details/', views.order_details, name="order_details"),

    # payments
    path('order_view/', views.order_view, name="order_view"),
    path('proceeds_to_pay/', views.proceeds_to_pay, name="proceeds_to_pay"),
    path('payment/<int:id>', views.payment, name="payment"),
    path('get_payment/', views.get_payment, name="get_payment"),
    path('recived_pay/', views.recived_pay, name="recived_pay"),
    # tracker
    path('Tracker/', views.tracker, name="tracker"),
    path('track_product/', views.track_product, name="track_product"),

]
