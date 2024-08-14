from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, RegistroUsuario, ActiveUsersCountView

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
# router.register(r'_personas', UserDetailView)

urlpatterns = [
    path('', include(router.urls)),
    #path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('registro/', RegistroUsuario.as_view(), name='registro_usuario'),
    path('active-users-count/', ActiveUsersCountView.as_view(), name='active-users'),
]
