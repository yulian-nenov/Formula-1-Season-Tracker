from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts import views

app_name = "accounts"

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='detail'),
    path('login/', LoginView.as_view(template_name='accounts/account_form.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]