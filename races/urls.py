from django.urls import path, include

from races import views

app_name = 'races'



races_urls = [
    path('', views.RaceListView.as_view(), name='race_list'),
    path('create/', views.RaceCreateView.as_view(), name='race_create'),
    path('<int:pk>/', include([
        path('', views.RaceDetailView.as_view(), name='race_details'),
        path('edit/', views.RaceUpdateView.as_view(), name='race_edit'),
        path('delete/', views.RaceDeleteView.as_view(), name='race_delete'),
    ]))
]

results_urls = [
    path('', views.ResultCreateView.as_view(), name='result_add'),
    path('<int:pk>/', include([
        path('edit/', views.ResultUpdateView.as_view(), name='result_edit'),
        path('delete/', views.ResultDeleteView.as_view(), name='result_delete'),
    ])),
]

urlpatterns = [
    path('races/', include(races_urls)),
    path('results/', include(results_urls)),
    path('standings/', views.StandingsView.as_view(), name='standings'),
]
