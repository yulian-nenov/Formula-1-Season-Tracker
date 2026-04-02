from celery import shared_task
from django.db.models import Sum
from drivers.models import Driver

@shared_task
def recalculate_driver_stats_task(driver_id):
    try:
        driver = Driver.objects.get(pk=driver_id)
        results = driver.results.all()

        driver.total_points = (results.aggregate(total=Sum("points_awarded"))["total"] or 0)
        driver.wins = results.filter(finishing_position=1).count()
        driver.podiums = results.filter(finishing_position__lte=3).count()
        driver.dnfs = results.filter(status="DNF").count()

        driver.save()
    except Driver.DoesNotExist:
        pass
