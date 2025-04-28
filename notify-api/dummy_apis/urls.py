from django.urls import path
from .views import DummyAPI1, DummyAPI2

urlpatterns = [
    path('dummy-api-1/', DummyAPI1.as_view(), name='dummy-api-1'),
    path('dummy-api-2/', DummyAPI2.as_view(), name='dummy-api-2'),
]