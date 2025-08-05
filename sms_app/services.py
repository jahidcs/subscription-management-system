from rest_framework.exceptions import ValidationError
from django.db import transaction
from datetime import datetime, timedelta
from .models import Subscription, Plan


class SubscriptionService:
    @staticmethod
    def has_active_subscription(user, plan) -> bool:
        if Subscription.objects.filter(user=user, plan=plan, status='active').exists():
            return False
        return True

    @staticmethod
    def end_date_for_plan(plan) -> datetime:
        return datetime.now() + timedelta(days=plan.duration_days)

    @staticmethod
    def create_subscription(user, data) -> Subscription:
        plan_id = data.get('plan_id')
        try:
            plan = Plan.objects.get(id=plan_id)
        except Plan.DoesNotExist:
            raise ValidationError("Invalid plan ID")
        
        can_subscribe = SubscriptionService.has_active_subscription(user, plan)
        if not can_subscribe:
            raise ValidationError("User already has an active subscription for this plan")
        end_date = SubscriptionService.end_date_for_plan(plan)
        
        try:
            with transaction.atomic():
                subscription = Subscription.objects.create(
                    user=user,
                    plan=plan,
                    end_date=end_date,
                    status='active'
                )
            return subscription
        except Exception as e:
            raise ValidationError(f"Failed to create subscription: {str(e)}")
        
    @staticmethod
    def get_user_subscriptions(user):
        return Subscription.objects.filter(user=user).select_related('plan')
    
    @staticmethod
    def cancel_subscription(user, data):
        subscription_id = data.get('subscription_id')
        try:
            subscription = Subscription.objects.get(id=subscription_id, user=user)
        except Subscription.DoesNotExist:
            raise ValidationError("Subscription not found.")
        
        if subscription.status != 'active':
            raise ValidationError("Subscription is not active or already cancelled.")
        
        subscription.status = 'cancelled'
        subscription.save()
        
        return subscription