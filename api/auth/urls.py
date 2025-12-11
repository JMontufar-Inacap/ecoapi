from django.urls import path
from .views import EmailTokenObtainPairView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("token/", EmailTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('login_jwt/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]