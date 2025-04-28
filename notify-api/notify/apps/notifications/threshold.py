from django.utils.timezone import now, timedelta
from .logs import logger
from .models import FailureLog, NotificationRule
from .utils.email_sender import send_failure_notification
from .utils.sms_sender import MockSMSService

from .logs import create_failure_log

def handle_threshold_logic(data, serializer):
    api_name = data.get('api_name')
    failure_details = data.get('failure_details')
    notification_method = data.get('notification_method')

    try:
        rule = NotificationRule.objects.get(api_name=api_name)
    except NotificationRule.DoesNotExist:
        raise ValueError(f"No notification rule found for API: {api_name}")

    # Check threshold
    recent_notifications = FailureLog.objects.filter(
        timestamp__gte=now() - timedelta(minutes=rule.frequency),
        api_name=api_name
    ).count()

    if recent_notifications >= rule.threshold:
        # Log suppressed notification
        logger.warning(f"Notification suppressed for {api_name} due to threshold.")
        create_failure_log(
            api_name=api_name,
            error_message=f"Notification suppressed due to threshold. Details: {failure_details}",
            severity="critical",
            notification_method="none"
        )
        return False  # Notification not sent

    # Send notifications based on the specified method
    if notification_method in ['email', 'both']:
        send_failure_notification(f"API: {api_name}, Details: {failure_details}")
    if notification_method in ['sms', 'both']:
        sms_service = MockSMSService(from_number="mock_sender_number")
        sms_service.send_sms("mock_recipient_number", f"API: {api_name}, Details: {failure_details}")

    # Log valid notification
    create_failure_log(
        api_name=api_name,
        error_message=failure_details,
        severity="high",
        notification_method=notification_method
    )
    return True  # Notification sent