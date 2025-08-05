from django.urls import path
from .views import (
    SubscribeView,
    SubscriptionListView,
    SubscriptionCancelView,
    ExchangeRateLatestView,
)

urlpatterns = [
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),
    path('subscriptions/', SubscriptionListView.as_view(), name='subscribtion-list'),
    path('cancel/', SubscriptionCancelView.as_view(), name='cancel-subscription'),
    path('exchange-rate/', ExchangeRateLatestView.as_view(), name='exchange-rate-latest'),
]