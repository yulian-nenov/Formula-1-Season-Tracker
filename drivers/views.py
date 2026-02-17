from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from drivers.forms import DriverCreateForm, DriverEditForm, DriverDeleteForm
from drivers.models import Driver
from races.models import Result


def driver_list(request: HttpRequest) -> HttpResponse:
    drivers = Driver.objects.all()

    context = {
        'drivers': drivers,
    }

    return render(request, 'drivers/list.html', context)

def driver_details(request: HttpRequest, pk: int) -> HttpResponse:
    driver = Driver.objects.get(pk=pk)
    recent_results = Result.objects.filter(driver=driver).order_by('-id')[:3]

    context = {
        'driver': driver,
        'recent_results': recent_results,
    }

    return render(request, 'drivers/detail.html', context)

def driver_create(request: HttpRequest) -> HttpResponse:
    form = DriverCreateForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        form.save()

        return redirect('drivers:list')

    context = {
        'form': form,
        'page_title': 'Create Driver',
        'button_text': 'Create Driver'
    }

    return render(request, 'drivers/driver-form.html', context)

def driver_edit(request: HttpRequest, pk: int) -> HttpResponse:
    driver = Driver.objects.get(pk=pk)
    form = DriverEditForm(request.POST or None, request.FILES or None, instance=driver)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('drivers:details', driver.pk)

    context = {
        'form': form,
        'page_title': 'Edit Driver',
        'button_text': 'Edit Driver'
    }

    return render(request, 'drivers/driver-form.html', context)

def driver_delete(request: HttpRequest, pk: int) -> HttpResponse:
    driver = Driver.objects.get(pk=pk)
    form = DriverDeleteForm(request.POST or None, request.FILES or None, instance=driver)

    if request.method == 'POST' and form.is_valid():
        driver.delete()
        return redirect('drivers:list')

    context = {
        'form': form,
        'page_title': 'Delete Driver',
        'button_text': 'Delete Driver'
    }

    return render(request, 'drivers/driver-form.html', context)
