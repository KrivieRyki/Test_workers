from rest_framework import viewsets
from datetime import timedelta
from django.db.models import F, Case, When, ExpressionWrapper, DurationField, IntegerField, Value
from django.db.models.functions import Coalesce, Greatest
from .models import DriverLog
from rest_framework.response import Response
from datetime import timedelta, datetime


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
            working_hours, working_remainder = divmod(times['working_time'].total_seconds(), 3600)
            working_minutes, working_seconds = divmod(working_remainder, 60)

            resting_hours, resting_remainder = divmod(times['resting_time'].total_seconds(), 3600)
            resting_minutes, resting_seconds = divmod(resting_remainder, 60)

            off_hours, off_remainder = divmod(times['off_time'].total_seconds(), 3600)
            off_minutes, off_seconds = divmod(off_remainder, 60)

            result.append({
                'company_id': times['company_id'],
                'driver_id': driver_id,
                'working_time': f'{int(working_hours)} hours, {int(working_minutes)} minutes, {int(working_seconds)} seconds',
                'resting_time': f'{int(resting_hours)} hours, {int(resting_minutes)} minutes, {int(resting_seconds)} seconds',
                'off_time': f'{int(off_hours)} hours, {int(off_minutes)} minutes, {int(off_seconds)} seconds'
            })

        return Response(result)


class DriverLogWeeklyViewSet(viewsets.ViewSet):
    def list(self, request):
        week_start = datetime.now() - timedelta(days=datetime.now().weekday())
        queryset = DriverLog.objects.filter(create_date__gte=week_start)

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
            working_hours, working_remainder = divmod(times['working_time'].total_seconds(), 3600)
            working_minutes, working_seconds = divmod(working_remainder, 60)

            resting_hours, resting_remainder = divmod(times['resting_time'].total_seconds(), 3600)
            resting_minutes, resting_seconds = divmod(resting_remainder, 60)

            off_hours, off_remainder = divmod(times['off_time'].total_seconds(), 3600)
            off_minutes, off_seconds = divmod(off_remainder, 60)

            result.append({
                'company_id': times['company_id'],
                'driver_id': driver_id,
                'working_time': f'{int(working_hours)} hours, {int(working_minutes)} minutes, {int(working_seconds)} seconds',
                'resting_time': f'{int(resting_hours)} hours, {int(resting_minutes)} minutes, {int(resting_seconds)} seconds',
                'off_time': f'{int(off_hours)} hours, {int(off_minutes)} minutes, {int(off_seconds)} seconds'
            })

        return Response(result)
