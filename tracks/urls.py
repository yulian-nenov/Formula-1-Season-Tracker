from django.urls import path, include

from tracks import views

app_name = 'tracks'

urlpatterns = [
    path('', views.TrackListView.as_view(), name='list'),
    path('create/', views.TrackCreateView.as_view(), name='create'),
    path('<int:pk>/', include([
        path('', views.TrackDetailView.as_view(), name='details'),
        path('edit/', views.TrackUpdateView.as_view(), name='edit'),
        path('delete/', views.TrackDeleteView.as_view(), name='delete'),
    ])),
]
