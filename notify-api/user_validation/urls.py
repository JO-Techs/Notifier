from django.urls import path
from .views import ValidateUserAgeView

urlpatterns = [
    path('validate-age/<int:user_id>/', ValidateUserAgeView.as_view(), name='validate-age'),
]