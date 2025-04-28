from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from notify.apps.notifications.logs import create_failure_log
from notify.apps.notifications.models import NotificationRule
from notify.apps.notifications.threshold import handle_threshold_logic
from .serializers import DummyAPI1Serializer, DummyAPI2Serializer

from django.shortcuts import render

class DummyAPI1(APIView):
    def get(self, request):
        return render(request, 'dummy_api1_age_validation.html')

    def post(self, request):
        serializer = DummyAPI1Serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        age = serializer.validated_data.get('age')
        if age < 18:
            failure_details = f"Age validation failed. Provided age: {age}."

            # Fetch the notification rule for Dummy API 1
            try:
                rule = NotificationRule.objects.get(api_name='Dummy API 1')
                notification_method = rule.notification_method
            except NotificationRule.DoesNotExist:
                return Response(
                    {"error": "Notification rule not found for Dummy API 1."},
                    status=status.HTTP_404_NOT_FOUND
                )

            data = {
                'api_name': 'Dummy API 1',
                'failure_details': failure_details,
                'notification_method': notification_method
            }

            # Handle threshold logic
            if not handle_threshold_logic(data, serializer):
                return Response(
                    {"error": "Notification suppressed due to threshold."},
                    status=status.HTTP_200_OK
                )

            return Response(
                {"message": "Failure logged and notification sent."},
                status=status.HTTP_201_CREATED
            )

        return Response({"message": "Age is valid."}, status=status.HTTP_200_OK)
    
class DummyAPI2(APIView):
    def get(self, request):
        return render(request, 'dummy_api2_data_validation.html')

    def post(self, request):
        serializer = DummyAPI2Serializer(data=request.data)
        if not serializer.is_valid():
            # Prepare failure details
            failure_details = f"Invalid input received: {request.data.get('field_value')}. Error: {serializer.errors.get('field_value')}"
            try:
                rule = NotificationRule.objects.get(api_name='Dummy API 2')
                notification_method = rule.notification_method 
            except NotificationRule.DoesNotExist:
                return Response(
                    {"error": "Notification rule not found for Dummy API 2."},
                    status=status.HTTP_404_NOT_FOUND
                )            
            data = {
                'api_name': 'Dummy API 2',
                'failure_details': failure_details,
                'notification_method': notification_method
            }

            # Handle threshold logic
            if not handle_threshold_logic(data, serializer):
                return Response(
                    {"error": "Notification suppressed due to threshold."},
                    status=status.HTTP_200_OK
                )

            # Log the failure
            '''create_failure_log(
                api_name='Dummy API 2',
                error_message=failure_details,
                severity='critical',
                notification_method=notification_method,
            )'''
            return Response(
                {"message": "Failure logged and notification sent."},
                status=status.HTTP_201_CREATED
            )

        # If the input is valid, return a success response
        return Response({"message": "Field value is valid."}, status=status.HTTP_200_OK)