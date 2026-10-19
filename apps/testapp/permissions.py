from rest_framework.permissions import BasePermission, SAFE_METHODS
from apps.testapp.models import User


class IsTeacherOrReadOnly(BasePermission):
    """
    Чтение разрешено авторизованным пользователям.
    Изменение данных разрешено только преподавателям.
    """

    def has_permission(self, request, view):
        # Проверяем авторизацию
        if not request.user or not request.user.is_authenticated:
            return False

        # GET, HEAD и OPTIONS доступны всем авторизованным
        if request.method in SAFE_METHODS:
            return True

        # Изменение данных доступно только преподавателям
        return request.user.role == User.Role.TEACHER