from django.urls import path, include

from races.views import race_list, race_details, race_create, race_edit, race_delete, \
    result_add, result_edit, result_delete, standings

app_name = 'races'



races_urls = [
    path('', race_list, name='race_list'),
    path('create/', race_create, name='race_create'),
    path('<int:pk>/', include([
        path('', race_details, name='race_details'),
        path('edit/', race_edit, name='race_edit'),
        path('delete/', race_delete, name='race_delete'),
    ]))
]

results_urls = [
    path('', result_add, name='result_add'),
    path('<int:pk>/', include([
        path('edit/', result_edit, name='result_edit'),
        path('delete/', result_delete, name='result_delete'),
    ])),
]

urlpatterns = [
    path('races/', include(races_urls)),
    path('results/', include(results_urls)),
    path('standings/', standings, name='standings'),
]
