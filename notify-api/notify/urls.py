from django.contrib import admin
from django.urls import include, path

from notify.apps.notifications.views import (
    FailureNotificationView,
    FailureLogListView,
    NotificationRuleListView,
    NotificationRuleCreateView,
    NotificationRuleDeleteView,
    failure_logs_view,
    manage_rules_view
)

urlpatterns = [
    path('manage-rules/', manage_rules_view, name='manage-rules'),
    path('failure-logs/', failure_logs_view, name='failure-logs'),
    path('api/failure-logs/', FailureLogListView.as_view(), name='api-failure-logs'),
    path('api/notification-rules/', NotificationRuleListView.as_view(), name='api-notification-rules'),
    path('api/notification-rules/create/', NotificationRuleCreateView.as_view(), name='api-create-rule'),
    path('api/notification-rules/delete/<int:pk>/', NotificationRuleDeleteView.as_view(), name='api-delete-rule'),
    path('notify-failure/', FailureNotificationView.as_view(), name='notify-failure'),
    path('dummy-apis/', include('dummy_apis.urls')),
    path('admin/', admin.site.urls),
]