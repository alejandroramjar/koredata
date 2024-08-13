import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.core.cache import cache
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import viewsets, generics, status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Usuario
from .serializers import UsuarioSerializer, RegisterSerializer

logger = logging.getLogger(__name__)


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

    def handle_exception(self, exc):
        logger.error(f"Error en UsuarioViewSet: {exc}")
        return super().handle_exception(exc)


class RegistroUsuario(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        user.is_active = False  # Establecer el usuario como inactivo
        user.save()

        logger.info(f"Usuario registrado exitosamente: {user.username}")

        # Enviar correo electrónico al usuario
        self.send_registration_email(user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def send_registration_email(self, user):
        try:
            send_mail(
                'Registro exitoso',
                f'Hola {user.username}, tu registro ha sido exitoso. El administrador del sistema tiene 72 horas para autorizar tu cuenta.',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            send_mail(
                'Nuevo registro de usuario',
                f'El usuario {user.username} se ha registrado y está pendiente de autorización. Tienes 72 horas para autorizar el registro.',
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f"Error al enviar correos: {e}")


class ActiveUsersCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        User = get_user_model()
        request_count = cache.get('request_count', 0)
        sessions = Session.objects.filter(expire_date__gte=timezone.now())
        user_ids = [session.get_decoded().get('_auth_user_id') for session in sessions]
        user_auth_count = len(set(user_ids))
        user_count = User.objects.filter(is_active=True).count()
        return Response({'count': user_count, 'user_auth_count': user_auth_count, 'request_count': request_count})
