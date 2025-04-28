from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from django.utils.timezone import now, timedelta

from .models import FailureLog, NotificationRule
from .serializers import FailureLogSerializer, NotificationRuleSerializer
from .utils.email_sender import send_failure_notification
from .utils.sms_sender import MockSMSService
from .logs import create_failure_log, logger
from .threshold import handle_threshold_logic
from .NotificationRulesCRUD import create_or_update_notification_rule


# Frontend Views
def frontend_view(request):
    return render(request, 'index.html')


def failure_logs_view(request):
    """Render failure logs in the frontend."""
    logs = FailureLog.objects.all().order_by('-timestamp')
    return render(request, 'failure_logs.html', {'logs': logs})


def manage_rules_view(request):
    """Render and manage notification rules."""
    if request.method == 'POST':
        if 'delete_rule' in request.POST:
            rule_id = request.POST.get('rule_id')
            NotificationRule.objects.filter(id=rule_id).delete()
            return redirect('manage-rules')

        # Create or update the rule
        try:
            create_or_update_notification_rule(request.POST)
            return redirect('manage-rules')
        except ValueError as e:
            return render(request, 'manage_rules.html', {'rules': NotificationRule.objects.all(), 'error': str(e)})



    rules = NotificationRule.objects.all()
    return render(request, 'manage_rules.html', {'rules': rules})


# API Views
class FailureLogListView(ListAPIView):
    """List all failure logs."""
    queryset = FailureLog.objects.all().order_by('-timestamp')
    serializer_class = FailureLogSerializer


class NotificationRuleListView(ListAPIView):
    """List all notification rules."""
    queryset = NotificationRule.objects.all()
    serializer_class = NotificationRuleSerializer


class NotificationRuleCreateView(CreateAPIView):
    """Create or update a notification rule."""
    queryset = NotificationRule.objects.all()
    serializer_class = NotificationRuleSerializer


class NotificationRuleDeleteView(DestroyAPIView):
    """Delete a notification rule."""
    queryset = NotificationRule.objects.all()
    serializer_class = NotificationRuleSerializer


class FailureNotificationView(APIView):
    """Handle failure notifications."""
    def post(self, request):
        api_name = request.data.get('api_name')
        failure_details = request.data.get('failure_details')
        notification_method = request.data.get('notification_method')

        if not api_name or not failure_details:
            logger.error("API name or failure details missing in the request.")
            return Response({"error": "API name and failure details are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            rule = NotificationRule.objects.get(api_name=api_name)
            logger.info(f"NotificationRule found for {api_name}: {rule.notification_method}, Threshold: {rule.threshold}, Frequency: {rule.frequency}")
        except NotificationRule.DoesNotExist:
            logger.error(f"No NotificationRule found for {api_name}.")
            return Response({"error": f"No notification rule found for API: {api_name}"}, status=status.HTTP_404_NOT_FOUND)

        # Handle threshold logic
        data = {
            'api_name': api_name,
            'failure_details': failure_details,
            'notification_method': notification_method or rule.notification_method
        }
        if not handle_threshold_logic(data, None):
            return Response({"error": "Max notification limit reached for this API. Notification suppressed."}, status=status.HTTP_200_OK)

        return Response({"message": "Notification sent successfully."}, status=status.HTTP_200_OK)