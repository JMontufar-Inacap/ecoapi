# api/exceptions.py
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

def custom_exception_handler(exc, context):
    """
    Maneja errores personalizados en DRF.
    """
    # Llamamos al handler por defecto primero
    response = exception_handler(exc, context)

    if response is not None:
        # Modificamos el contenido
        data = {}

        if response.status_code == 400:
            data['mensaje'] = "Error de validación"
            data['detalles'] = response.data
        elif response.status_code == 401:
            data['mensaje'] = "No autenticado: credenciales inválidas"
            data['detalles'] = response.data
        elif response.status_code == 403:
            data['mensaje'] = "No autorizado: no tienes permisos"
            data['detalles'] = response.data
        elif response.status_code == 404:
            data['mensaje'] = "No encontrado: recurso inexistente"
            data['detalles'] = response.data
        elif response.status_code == 500:
            data['mensaje'] = "Error interno del servidor"
            data['detalles'] = str(exc)
        else:
            data['mensaje'] = "Error"
            data['detalles'] = response.data

        return Response(data, status=response.status_code)
    
    # En caso de que response sea None (ej: ObjectDoesNotExist)
    if isinstance(exc, ObjectDoesNotExist):
        return JsonResponse({'mensaje':'No encontrado: objeto inexistente','status_code':404}, status=404)

    # Si es un error no manejado
    return JsonResponse({'mensaje':'Error interno del servidor','status_code':500}, status=500)
 