from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from accounts import views

app_name = "accounts"

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('edit/', views.ProfileUpdateView.as_view(), name='edit'),
    path('delete/', views.UserDeleteView.as_view(), name='delete'),
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='detail'),
    path('login/', LoginView.as_view(template_name='accounts/account_form.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]