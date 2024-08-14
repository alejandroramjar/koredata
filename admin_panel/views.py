import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.core.cache import cache
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import viewsets, generics, status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenVerifyView

from .models import Usuario
from .serializers import UsuarioSerializer

logger = logging.getLogger(__name__)



class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            return response
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def handle_exception(self, exc):
        logger.error(f"Error en UsuarioViewSet: {exc}")
        return super().handle_exception(exc)

    def retrieve(self, request, *args, **kwargs):
        try:
            response = super().retrieve(request, *args, **kwargs)
            logger.info(f"Detalles del usuario obtenidos para el ID: {kwargs['pk']}")
            return response
        except Exception as e:
            logger.critical(f"Error inesperado al obtener los detalles del usuario: {e}")
            return Response({"error": "Error inesperado, por favor intente nuevamente más tarde."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            logger.info(f"Detalles del usuario actualizados para el ID: {kwargs['pk']}")
            return response
        except Exception as e:
            logger.critical(f"Error inesperado al actualizar los detalles del usuario: {e}")
            return Response({"error": f"Error inesperado, por favor intente nuevamente más tarde.{e.detail}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        try:
            logger.info(
                f'Solicitud de eliminación de usuario por parte del usuario: {request.user.username} al usuario {kwargs["pk"]}')
            if not request.user.is_superuser:
                logger.warning(f'El usuario {request.user.username} no tiene permitido eliminar a otros usuarios.')
                return Response({'error': 'El usuario no tiene permitido ejecutar esta acción.'},
                                status=status.HTTP_403_FORBIDDEN)
            response = super().destroy(request, *args, **kwargs)
            logger.info(f"Usuario eliminado con ID: {kwargs['pk']}")
            return response
        except Exception as e:
            logger.critical(f"Error inesperado al eliminar el usuario: {e}")
            return Response({"error": "Error inesperado, por favor intente nuevamente más tarde."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RegistroUsuario(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
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
        users_inactives = Usuario.objects.filter(is_active=False).count()
        users_actives = Usuario.objects.filter(is_active=True).count()
        request_count = cache.get('request_count', 0)
        sessions = Session.objects.filter(expire_date__gte=timezone.now())
        user_ids = [session.get_decoded().get('_auth_user_id') for session in sessions]
        user_auth_count = len(set(user_ids))
        user_auth_count += 1  # se le suma 1 porque obtiene el valor de un array.
        user_count = User.objects.filter(is_active=True).count()
        return Response({'count': user_count, 'user_auth_count': user_auth_count, 'request_count': request_count,
                         'users_actives': users_actives, 'users_inactives': users_inactives})

# class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Usuario.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]
#
#     @superuser_required
#     def get(self, request, *args, **kwargs):
#         try:
#             response = super().get(request, *args, **kwargs)
#             logger.info(
#                 f"Detalles del usuario obtenidos para el ID: {kwargs['pk']}")  # Registro de evento de obtención de detalles de usuario
#             return response
#         except Exception as e:
#             logger.critical(
#                 f"Error inesperado al obtener los detalles del usuario: {e}")  # Registro de evento de error crítico
#             return Response({"error": "Error inesperado, por favor intente nuevamente más tarde."},
#                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#     @superuser_required
#     def put(self, request, *args, **kwargs):
#         try:
#             response = super().put(request, *args, **kwargs)
#             logger.info(
#                 f"Detalles del usuario actualizados para el ID: {kwargs['pk']}")  # Registro de evento de actualización de detalles de usuario
#             return response
#         except Exception as e:
#             logger.critical(
#                 f"Error inesperado al actualizar los detalles del usuario: {e}")  # Registro de evento de error crítico
#             return Response({"error": "Error inesperado, por favor intente nuevamente más tarde."},
#                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#     @superuser_required
#     def delete(self, request, *args, **kwargs):
#         try:
#             logger.info(
#                 f'Solicitud de eliminación de usuario por parte del usuario: {request.user.username} al usuario {kwargs["pk"]}')
#             if not request.user.is_superuser:
#                 logger.warning(
#                     f'El usuario {request.user.username} no tiene permitido eliminar a otros usuarios.')
#                 return Response({'error': 'El usuario no permitido ejecutar esta acción.'},
#                                 status=status.HTTP_403_FORBIDDEN, )
#             response = super().delete(request, *args, **kwargs)
#             logger.info(f"Usuario eliminado con ID: {kwargs['pk']}")  # Registro de evento de eliminación de usuario
#             return response
#         except Exception as e:
#             logger.critical(f"Error inesperado al eliminar el usuario: {e}")  # Registro de evento de error crítico
#             return Response({"error": "Error inesperado, por favor intente nuevamente más tarde."},
#                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)
