from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


# Register your models here.

class UsuarioAdmin(UserAdmin):
    # Campos a mostrar en la lista de usuarios
    list_display = ('username', 'email', 'first_name', 'last_name', 'edad', 'cpf', 'is_staff')
    # Campos que se pueden buscar
    search_fields = ('username', 'email', 'first_name', 'last_name', 'cpf')
    # Filtros disponibles en la lista de usuarios
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    # Campos a mostrar en el formulario de edición de usuarios
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información Personal', {'fields': ('first_name', 'last_name', 'email', 'edad', 'cpf')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    # Campos a mostrar en el formulario de creación de usuarios
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
            'username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'edad', 'cpf', 'is_active',
            'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )
    # Orden de los usuarios en la lista
    ordering = ('username',)


admin.site.register(Usuario, UsuarioAdmin)
