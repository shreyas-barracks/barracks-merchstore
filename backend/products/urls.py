from django.urls import path
from . import views

urlpatterns = [
    path('product/all/', views.AllProductsView.as_view()),
    path('product/<int:product_id>/', views.ProductView.as_view()),
    path('cart/add/', views.AddToCart.as_view()),
    path('cart/view/', views.ViewCart.as_view()),
    path('cart/delete/', views.RemoveFromCart.as_view()),
    path('cart/update/', views.UpdateCart.as_view()),
    # VULN-V4W5X6 & VULN-Y7Z8A9: Unauthenticated product endpoints
    path('product/create/', views.CreateProductUnauthenticated.as_view()),
    path('product/toggle-orders/<int:product_id>/', views.ToggleProductOrders.as_view()),
    # VULN-K1L2M3: IDOR - Edit any user's cart
    path('cart/update/<int:user_id>/', views.UpdateCartIDOR.as_view()),
    # VULN-H7I8J9: Mass Assignment - Update product fields
    path('product/update/<int:product_id>/', views.UpdateProductMassAssignment.as_view()),
]
