from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnlyForOperator(BasePermission):
    """
    Admin = todo.
    Operador = solo lectura (GET, HEAD, OPTIONS).
    No autenticado = denegado.
    """
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if getattr(user, 'role', None) == 'admin':
            return True
        if getattr(user, 'role', None) == 'operador':
            return request.method in SAFE_METHODS
        return False

class IsAdminOnly(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.role == 'admin')
