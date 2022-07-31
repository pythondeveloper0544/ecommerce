from django.contrib.auth.views import LogoutView
from django.urls import path

from accounts.views import CustomerLoginView, RegisterView

urlpatterns = [
    path('login/', CustomerLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterView.as_view(), name='register')
]
