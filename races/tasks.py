from celery import shared_task
from races.models import Race
from drivers.models import Driver
from drivers.tasks import recalculate_driver_stats_task

@shared_task
def delete_all_races_task():
    driver_ids = list(Driver.objects.values_list('pk', flat=True))

    Race.objects.all().delete()
        
    for driver_id in driver_ids:
        recalculate_driver_stats_task.delay(driver_id)
