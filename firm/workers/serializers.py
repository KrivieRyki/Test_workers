from rest_framework import serializers


class DriverLogWeeklySerializer(serializers.Serializer):
    driver_id = serializers.IntegerField()
    working_time = serializers.DurationField()
    resting_time = serializers.DurationField()
    off_time = serializers.DurationField()
