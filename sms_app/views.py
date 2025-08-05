from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from .models import ExchangeRateLog
from .serializers import (
    SubscriptionSerializer,
    SubscribeRequestSerializer,
    CancelSubscriptionSerializer,
    ExchangeRateSerializer
)
from .services import SubscriptionService
from .pagination import GenericPagination


class SubscriptionListView(ListAPIView):
    serializer_class = SubscriptionSerializer
    pagination_class = GenericPagination

    def get_queryset(self):
        user = self.request.user
        return SubscriptionService.get_user_subscriptions(user)



class SubscribeView(APIView):
    def post(self, request):
        serializer = SubscribeRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            subscription = SubscriptionService.create_subscription(request.user, serializer.validated_data)
        except ValidationError as e:
            return Response(
                {
                    "error": "Validation error",
                    "details": e.detail
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    "error": "Exception occurred while creating subscription",
                    "details": e.detail
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        response_data = SubscriptionSerializer(subscription).data
        return Response(
            response_data,
            status=status.HTTP_201_CREATED
        )


class SubscriptionCancelView(APIView):
    def post(self, request):
        serializer = CancelSubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        try:
            cancel_subscription = SubscriptionService.cancel_subscription(user, serializer.validated_data)
            return Response(
                {
                    'message': 'Subscription cancelled successfully.',
                    'subscription_id': cancel_subscription.id
                },
                status=status.HTTP_200_OK
            )
        except ValidationError as e:
            return Response(
                {
                    "error": "Validation error",
                    "details": e.detail
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    "error": "Exception occurred while cancelling subscription",
                    "details": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ExchangeRateLatestView(APIView):
    def get(self, request):
        base = request.query_params.get("base", "USD")
        target = request.query_params.get("target", "BDT")

        if not base or not target:
            return Response(
                {
                    'error': 'Both base and target currencies are required.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        latest_log = ExchangeRateLog.objects.filter(
            base_currency=base.upper(),
            target_currency=target.upper()
        ).order_by('-fetched_at').first()

        serializer = ExchangeRateSerializer(latest_log)
        return Response(serializer.data, status=status.HTTP_200_OK)


from django.shortcuts import render
from .models import Subscription

def subscription_list_view(request):
    subscriptions = Subscription.objects.select_related('user', 'plan').all()
    return render(request, 'sms_app/subscriptions_list.html', {'subscriptions': subscriptions})