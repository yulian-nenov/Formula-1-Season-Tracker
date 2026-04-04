from django.db import migrations


def create_groups(apps, schema_editor):
    group = apps.get_model("auth", "Group")
    permission = apps.get_model("auth", "Permission")

    users_group, _ = group.objects.get_or_create(name="Users")
    track_admins_group, _ = group.objects.get_or_create(name="Track Admins")

    def get_perms(app_label, model_name):
        return permission.objects.filter(
            content_type__app_label=app_label,
            content_type__model=model_name,
        )

    # Users group — races, results, teams, drivers
    for app, model in [
        ("races", "race"),
        ("races", "result"),
        ("teams", "team"),
        ("drivers", "driver"),
    ]:
        users_group.permissions.add(*get_perms(app, model))

    # Track Admins group — tracks only
    track_admins_group.permissions.add(*get_perms("tracks", "track"))


def delete_groups(apps, schema_editor):
    group = apps.get_model("auth", "Group")
    group.objects.filter(name__in=["Users", "Track Admins"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_alter_profile_favorite_tracks_and_more"),
        ("drivers", "0004_driver_owner"),
        ("teams", "0003_team_owner"),
        ("races", "0005_result_owner"),
        ("tracks", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_groups, delete_groups),
    ]