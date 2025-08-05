
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from sms_app.views import subscription_list_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('sms_app.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('subscriptions/', subscription_list_view, name='subscriptions-list'),
]
