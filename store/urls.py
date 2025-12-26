from django.urls import path
from .views import product_list, create_product, update_product, delete_product, add_to_cart, cart_detail, remove_from_cart, update_cart_item

app_name = 'store'


urlpatterns = [
    path('products/', product_list, name='product_list'),
    path('products/create/', create_product, name='create_product'),
    path('products/update/<int:pk>/', update_product, name='update_product'),
    path('products/delete/<int:pk>/', delete_product, name='delete_product'),
    path('cartdetails/', cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),  # Add item to cart
    path('update/<int:item_id>/', update_cart_item, name='update_cart_item'),  # Update cart item
    path('remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),  # Ensure this exists
]