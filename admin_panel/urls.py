from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, RegistroUsuario, ActiveUsersCountView

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('registro/', RegistroUsuario.as_view(), name='registro_usuario'),
    path('active-users-count/', ActiveUsersCountView.as_view(), name='active-users'),
]
