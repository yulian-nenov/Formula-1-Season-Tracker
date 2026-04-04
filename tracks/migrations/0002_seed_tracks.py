from django.db import migrations


def create_tracks(apps, schema_editor):
    Track = apps.get_model('tracks', 'Track')
    Track.objects.bulk_create([
        Track(
            name='Monza',
            country='Italy',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Monza_track_map.svg/1920px-Monza_track_map.svg.png',
            length_km=5.79,
        ),
        Track(
            name='Silverstone',
            country='United Kingdom',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Silverstone_Circuit_vector_map.png/1920px-Silverstone_Circuit_vector_map.png',
            length_km=5.89,
        ),
        Track(
            name='Spa-Francorchamps',
            country='Belgium',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/Spa-Francorchamps_of_Belgium.svg/1920px-Spa-Francorchamps_of_Belgium.svg.png',
            length_km=7.00,
        ),
    ])


def delete_tracks(apps, schema_editor):
    Track = apps.get_model('tracks', 'Track')
    Track.objects.filter(id__in=[1, 2, 3]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_tracks, delete_tracks),
    ]