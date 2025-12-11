from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Departamento, Sensor, Evento, User
from .serializers import (
    DepartamentoSerializer,
    SensorSerializer,
    EventoSerializer,
    UserSerializer
)
from .permissions import IsAdminOrReadOnlyForOperator, IsAdminOnly

# USERS
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminOnly]  # solo admin CRUD usuarios

# DEPARTAMENTOS
class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnlyForOperator]

# SENSORES
class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.select_related('departamento', 'usuario').all()
    serializer_class = SensorSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnlyForOperator]

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def check_access(self, request):
        uid = request.data.get('uid') or request.query_params.get('uid')
        if not uid:
            return Response({"detail": "uid requerido"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            sensor = Sensor.objects.get(uid=uid)
        except Sensor.DoesNotExist:
            Evento.objects.create(sensor=None, accion='intento', resultado='denegado',
                                  notas=f'UID desconocido: {uid}')
            return Response({"result": "denegado", "reason": "UID no registrado"},
                            status=status.HTTP_404_NOT_FOUND)

        if sensor.estado != 'activo':
            Evento.objects.create(sensor=sensor, accion='intento', resultado='denegado',
                                  notas=f'Estado: {sensor.estado}')
            return Response({"result": "denegado", "reason": f"Sensor {sensor.estado}"},
                            status=status.HTTP_403_FORBIDDEN)

        Evento.objects.create(sensor=sensor, accion='intento', resultado='permitido',
                              notas='Acceso permitido')
        return Response({"result": "permitido", "sensor": SensorSerializer(sensor).data},
                        status=status.HTTP_200_OK)

# EVENTOS
class EventoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Evento.objects.select_related('sensor').all().order_by('-timestamp')
    serializer_class = EventoSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnlyForOperator]


# INFO
@api_view(['GET'])
@permission_classes([AllowAny])
def info_view(request):
    data = {
        "autor": "Josue Montufar",
        "asignatura": "Programación Back End",
        "proyecto": "Control de Accesos",
        "descripcion": "API para gestión de sensores RFID, eventos, departamentos y barrera de acceso.",
        "version": "1.0"
    }
    return Response(data)

# BARRERA
@api_view(['POST'])
@permission_classes([AllowAny])
def barrera_access(request):
    uid = request.data.get('uid')

    if not uid:
        return Response({"detail": "uid requerido"}, status=400)

    try:
        sensor = Sensor.objects.get(uid=uid)
    except Sensor.DoesNotExist:
        Evento.objects.create(
            sensor=None,
            accion='intento_barrera',
            resultado='denegado',
            notas=f"UID desconocido: {uid}"
        )
        return Response({"result": "denegado", "reason": "uid no registrado"}, status=404)

    if sensor.estado != 'activo':
        Evento.objects.create(
            sensor=sensor,
            accion='intento_barrera',
            resultado='denegado',
            notas=f"Sensor inactivo ({sensor.estado})"
        )
        return Response({"result": "denegado", "reason": "sensor inactivo"}, status=403)

    if sensor.usuario is None or not sensor.usuario.is_active:
        Evento.objects.create(
            sensor=sensor,
            accion='intento_barrera',
            resultado='denegado',
            notas=f"Usuario inactivo o no asignado"
        )
        return Response({"result": "denegado", "reason": "usuario inactivo"}, status=403)

    Evento.objects.create(
        sensor=sensor,
        accion='barrera_abierta',
        resultado='permitido',
        notas=f"Acceso OK"
    )

    return Response({
        "result": "permitido",
        "mensaje": "Barrera abierta",
        "sensor": SensorSerializer(sensor).data
    })


def custom_404(request, exception=None):
    return JsonResponse({'detail': 'Ruta no encontrada', 'status_code': 404}, status=404)
