from rest_framework import viewsets
from datetime import timedelta
from django.db.models import F, Case, When, ExpressionWrapper, DurationField, IntegerField, Value
from django.db.models.functions import Coalesce, Greatest
from .models import DriverLog
from rest_framework.response import Response
from datetime import timedelta, datetime
from django.utils import timezone


class DriverLogViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = DriverLog.objects.all()

        data = {}
        for log in queryset:
            if log.driver_id not in data:
                data[log.driver_id] = {
                    'company_id': log.company_id,
                    'working_time': timedelta(),
                    'resting_time': timedelta(),
                    'off_time': timedelta(),
                    'current_status': log.status,
                    'current_status_time': log.create_date
                }

            else:
                current_status_time = data[log.driver_id]['current_status_time']
                time_diff = log.create_date - current_status_time

                if data[log.driver_id]['current_status'] == 'working':
                    data[log.driver_id]['working_time'] += time_diff
                elif data[log.driver_id]['current_status'] == 'resting':
                    data[log.driver_id]['resting_time'] += time_diff
                elif data[log.driver_id]['current_status'] == 'off':
                    data[log.driver_id]['off_time'] += time_diff

                data[log.driver_id]['current_status'] = log.status
                data[log.driver_id]['current_status_time'] = log.create_date

        result = []
        for driver_id, times in data.items():
            working_time = format_timedelta(times['working_time'])
            resting_time = format_timedelta(times['resting_time'])
            off_time = format_timedelta(times['off_time'])

            result.append({
                'company_id': times['company_id'],
                'driver_id': driver_id,
                'working_time': working_time,
                'resting_time': resting_time,
                'off_time': off_time
            })

        return Response(result)


class DriverLogWeeklyViewSet(viewsets.ViewSet):
    def list(self, request):
        now = timezone.now()

        days_since_monday = now.weekday()
        week_start = now - timedelta(days=days_since_monday)
        queryset = DriverLog.objects.filter(create_date__gte=week_start)

        data = {}
        for log in queryset:
            print(f"Processing log for driver {log.driver_id}, status: {log.status}, create_date: {log.create_date}")
            if log.driver_id not in data:
                data[log.driver_id] = {
                    'company_id': log.company_id,
                    'working_time': timedelta(),
                    'resting_time': timedelta(),
                    'off_time': timedelta(),
                    'current_status': log.status,
                    'current_status_time': log.create_date
                }
            else:
                current_status_time = data[log.driver_id]['current_status_time']
                time_diff = log.create_date - current_status_time

                if data[log.driver_id]['current_status'] == 'working':
                    data[log.driver_id]['working_time'] += time_diff
                elif data[log.driver_id]['current_status'] == 'resting':
                    data[log.driver_id]['resting_time'] += time_diff
                elif data[log.driver_id]['current_status'] == 'off':
                    data[log.driver_id]['off_time'] += time_diff

                data[log.driver_id]['current_status'] = log.status
                data[log.driver_id]['current_status_time'] = log.create_date

        result = []
        for driver_id, times in data.items():
            working_time = format_timedelta(times['working_time'])
            resting_time = format_timedelta(times['resting_time'])
            off_time = format_timedelta(times['off_time'])

            result.append({
                'company_id': times['company_id'],
                'driver_id': driver_id,
                'working_time': working_time,
                'resting_time': resting_time,
                'off_time': off_time
            })

        return Response(result)


def format_timedelta(td):
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f'{hours} hours, {minutes} minutes, {seconds} seconds'
