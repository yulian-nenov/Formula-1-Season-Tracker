from django.urls import path, include

from teams.views import team_list, team_details, team_edit, team_create, team_delete

app_name='teams'

urlpatterns = [
    path('', team_list, name='list'),
    path('create/', team_create, name='create'),
    path('<int:pk>/', include([
        path('', team_details, name='details'),
        path('edit/', team_edit, name='edit'),
        path('delete/', team_delete, name='delete'),
    ]))
]
