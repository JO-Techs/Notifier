import logging
from .models import FailureLog

logger = logging.getLogger(__name__)

def get_failure_logs():
    # Fetch failure logs
    return FailureLog.objects.all().order_by('-timestamp')

def create_failure_log(api_name, error_message, severity="critical", notification_method="none"):
    try:
        log = FailureLog.objects.create(
            api_name=api_name,
            error_message=error_message,
            severity=severity,
            notification_method=notification_method
        )
        logger.info(f"Failure log created: {log}")
        return log
    except Exception as e:
        logger.error(f"Error creating failure log: {str(e)}")
        raise