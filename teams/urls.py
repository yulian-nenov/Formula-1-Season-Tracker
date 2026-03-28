from django.urls import path, include

from teams.views import team_edit
from teams import views

app_name='teams'

urlpatterns = [
    path('', views.TeamListView.as_view(), name='list'),
    path('create/', views.TeamCreateView.as_view(), name='create'),
    path('<int:pk>/', include([
        path('', views.TeamDetailsView.as_view(), name='details'),
        path('edit/', team_edit, name='edit'),
        path('delete/', views.TeamDeleteView.as_view(), name='delete'),
    ]))
]
