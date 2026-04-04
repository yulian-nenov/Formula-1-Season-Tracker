from rest_framework import serializers

from drivers.models import Driver


class DriverSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source='team.name', read_only=True)

    class Meta:
        model = Driver
        fields = ['id', 'name', 'nationality', 'age', 'rookie_status',
                  'image', 'team', 'team_name', 'wins', 'total_points',
                  'podiums', 'dnfs']
        read_only_fields = ['wins', 'total_points', 'podiums', 'dnfs']
