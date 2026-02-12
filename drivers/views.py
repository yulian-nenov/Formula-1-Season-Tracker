from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

def driver_list(request: HttpRequest) -> HttpResponse:
    return render(request, 'drivers/list.html')

def driver_details(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'drivers/detail.html')

def driver_create(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'drivers/create-driver.html')

def driver_edit(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'drivers/edit-driver.html')

def driver_delete(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'drivers/delete-driver.html')

