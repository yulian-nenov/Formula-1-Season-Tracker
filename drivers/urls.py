from django.urls import path, include

from drivers.views import driver_list, driver_create, driver_details, driver_edit, driver_delete

app_name = 'drivers'

urlpatterns = [
    path('', driver_list, name='list'),
    path('create/', driver_create, name='create'),
    path('<int:pk>/', include([
        path('', driver_details, name='details'),
        path('edit/', driver_edit, name='edit'),
        path('delete/', driver_delete, name='delete'),
    ]))
]
