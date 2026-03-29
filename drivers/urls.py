from django.urls import path, include

from drivers import views

app_name = 'drivers'

urlpatterns = [
    path('', views.DriverListView.as_view(), name='list'),
    path('create/', views.DriverCreateView.as_view(), name='create'),
    path('<int:pk>/', include([
        path('', views.DriverDetailsView.as_view(), name='details'),
        path('edit/', views.DriverUpdateView.as_view(), name='edit'),
        path('delete/', views.DriverDeleteView.as_view(), name='delete'),
    ]))
]
