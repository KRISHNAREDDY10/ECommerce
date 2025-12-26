from django.urls import path
from .views import home_page, register_view, login_view, logout_view

urlpatterns = [
    path('', home_page, name='home'),
    path('register/', register_view, name='register'),  # Registration URL
    path('login/', login_view, name='login'),  # Login URL
    path('logout/', logout_view, name='logout'),  # Logout URL
]
