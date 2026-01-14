from django.urls import path
from . import views

urlpatterns = [
    path("",views.home),
    path("ViewCakes/<cid>",views.viewCakes),
    path("ViewDetails/<cake_id>",views.viewDetails),
    path("SignUp",views.signUp),
    path("LogIn",views.logIn),
    path("LogOut",views.logOut),
    path("MyCart",views.showCart),
    path("EditCartItem/<item_id>",views.editCartItem),
    path("DeleteCartItem/<item_id>",views.deleteCartItem),
    path("ClearCart",views.clearCart),
    path("OrderSingleCake/<cart_id>/<price>",views.orderSingleCake),
    path("BuyCart/<price>",views.orderWholeCart),
    path("OrderHistory",views.getOrderHistory),
    path("ResetPassword",views.resetPassword),
    path("ClearHistory",views.clearHistory),
    path("FilterPrice",views.get_FilterCakesByPrice)
]