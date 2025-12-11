# api/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import DepartamentoViewSet, SensorViewSet, EventoViewSet, UserViewSet, info_view, barrera_access
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin
from .models import User, Departamento, Sensor, Evento
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

router = DefaultRouter()
router.register(r'departamentos', DepartamentoViewSet)
router.register(r'sensores', SensorViewSet, basename='sensors')
router.register(r'eventos', EventoViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('info/', info_view, name='api-info'),
    path('auth/', include('api.auth.urls')),
    path('barrera/', barrera_access, name='barrera-access'),
    path('login_jwt/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh_jwt/', TokenRefreshView.as_view(), name='token_refresh'),
]

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Extras', {'fields': ('role',)}),
    )

admin.site.register(Departamento)
admin.site.register(Sensor)
admin.site.register(Evento)