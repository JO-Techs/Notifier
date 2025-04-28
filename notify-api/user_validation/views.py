from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from .models import User

class ValidateUserAgeView(APIView):
    def post(self, request, user_id):
        # Get the user
        user = get_object_or_404(User, id=user_id)

        # Check if the user's age is less than 18
        if user.age < 18:
            # Prepare failure details
            failure_details = f"User {user.name} is under 18 years old (Age: {user.age})."

            # Send failure details to the notify-api
            notify_response = requests.post(
                'http://localhost:8000/notify-failure/',  # URL of the notify-api
                json={
                    'failure_type': 'Age Validation Failure',
                    'notification_method': 'both',  # Default to both email and SMS
                    'failure_details': failure_details,
                }
            )

            # Return the response from the notify-api
            if notify_response.status_code == 200:
                return Response({"message": "Failure notification sent successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Failed to send failure notification."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "User age is valid."}, status=status.HTTP_200_OK)