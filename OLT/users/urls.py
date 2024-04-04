from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import (UserCreateAPIView, UserListAPIView, UserDestroyAPIView, UserUpdateAPIView,
                         UserDetailAPIView, PaymentsCreateAPIView, PaymentsViewSet)

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'payment', PaymentsViewSet, basename='payment')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', UserListAPIView.as_view(), name='user-list'),
    path('create/', UserCreateAPIView.as_view(), name='user-create'),
    path('<int:pk>/', UserDetailAPIView.as_view(), name='user-get'),
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='user-update'),
    path("delete/<int:pk>/", UserDestroyAPIView.as_view(), name='user-delete'),
    path('payment/create/',  PaymentsCreateAPIView.as_view(), name='payment_create')
] + router.urls

