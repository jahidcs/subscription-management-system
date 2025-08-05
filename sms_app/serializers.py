from rest_framework import serializers
from .models import Subscription, Plan, ExchangeRateLog


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer()

    class Meta:
        model = Subscription
        fields = '__all__'


class SubscribeRequestSerializer(serializers.Serializer):
    plan_id = serializers.IntegerField()


class CancelSubscriptionSerializer(serializers.Serializer):
    subscription_id = serializers.IntegerField()


class ExchangeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRateLog
        fields = ['base_currency', 'target_currency', 'rate', 'fetched_at']
