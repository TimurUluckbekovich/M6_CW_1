from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from apps.testapp.models import User
from apps.testapp.serializers import GoogleAuthSerializer, UserSerializer
from apps.testapp.services import (
    get_google_access_token,
    get_google_user_info,
)
from apps.testapp.permissions import IsTeacherOrReadOnly


class GoogleAuthView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 1. Получаем code и обмениваем его на токен Google
        code = serializer.validated_data["code"]
        google_token = get_google_access_token(code)

        # 2. Получаем профиль пользователя Google
        user_info = get_google_user_info(google_token)
        email = user_info.get("email")

        if not email:
            return Response(
                {"error": "Google не предоставил email пользователя."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        email = email.strip().lower()

        # 3. Ищем пользователя или создаём нового студента
        user = User.objects.filter(email__iexact=email).first()
        is_new_user = False

        if not user:
            user = User.objects.create_user(
                email=email,
                role=User.Role.STUDENT,
            )
            is_new_user = True

        # 4. Генерируем внутренние JWT-токены
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "is_new_user": is_new_user,
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )


class LessonsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsTeacherOrReadOnly]

    def get(self, request):
        return Response(
            {"message": "Доступ к урокам разрешён.", "lessons": []},
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        return Response(
            {
                "message": "Урок успешно создан.",
                "lesson": request.data,
            },
            status=status.HTTP_201_CREATED,
        )