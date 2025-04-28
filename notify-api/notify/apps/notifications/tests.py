from django.test import TestCase
from django.urls import reverse
from .utils.email_sender import send_failure_notification
from .utils.sms_sender import MockSMSService
from .models import NotificationRule

class NotificationTests(TestCase):
    def setUp(self):
        # Initialize the mock SMS 
        NotificationRule.objects.create(
            api_name="Dummy API 1",
            notification_method="email",
            threshold=1,
            frequency=60
        )
        self.mock_sms_service = MockSMSService(from_number="mock_number")

    def test_email_notification(self):
        # Test the mocked email notification
        response = send_failure_notification("Test failure message")
        self.assertTrue(response)  # Assuming the function returns True on success

    def test_sms_notification(self):
        # Test the mocked SMS notification
        response = self.mock_sms_service.send_sms("+1234567890", "Test SMS Message")
        self.assertEqual(response, "mock_message_sid")  # Check the mock response

    def test_failure_notification_view(self):
    # Test the FailureNotificationView
        response = self.client.post(
            reverse('notify-failure'),  # Ensure the URL name matches your urlpatterns
            data={
                "api_name": "Dummy API 1",
                "failure_details": "Test failure message"
            },
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)  # Expecting a 200 status code
        self.assertContains(response, "Notification sent successfully.")  # Match the actual response content