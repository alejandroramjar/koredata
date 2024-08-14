from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'edad', 'cpf', 'is_active', 'is_staff']

    def validate_email(self, value):
        # Verificar si el correo electrónico ya está en uso por otro usuario
        if self.instance:
            print(value)
            if Usuario.objects.filter(email=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("Este correo electrónico ya está en uso.")
        else:
            if Usuario.objects.first(email=value).exists():
                raise serializers.ValidationError("Este correo electrónico ya está en uso.")
        return value

    def validate_username(self, value):
        # Verificar si el nombre de usuario ya está en uso por otro usuario
        if self.instance:
            if Usuario.objects.filter(username=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("Este nombre de usuario ya está en uso.")
        else:
            if Usuario.objects.filter(username=value).exists():
                raise serializers.ValidationError("Este nombre de usuario ya está en uso.")
        return value

    def validate_cpf(self, value):
        # Verificar si el CPF ya está en uso por otro usuario
        if self.instance:
            if Usuario.objects.filter(cpf=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("Este CPF ya está en uso.")
        else:
            if Usuario.objects.filter(cpf=value).exists():
                raise serializers.ValidationError("Este CPF ya está en uso.")
        return value

    def validate(self, data):
        # Verificar si ya existe un usuario con el mismo nombre y apellidos
        if self.instance:
            if Usuario.objects.filter(first_name=data['first_name'], last_name=data['last_name']).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("Ya existe un usuario con el mismo nombre y apellidos.")
        else:
            if Usuario.objects.filter(first_name=data['first_name'], last_name=data['last_name']).exists():
                raise serializers.ValidationError("Ya existe un usuario con el mismo nombre y apellidos.")
        return data

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.edad = validated_data.get('edad', instance.edad)
        instance.cpf = validated_data.get('cpf', instance.cpf)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.save()
        return instance

    def create(self, validated_data):
        user = Usuario(**validated_data)
        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()
        return user



class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'edad', 'cpf']

    def create(self, validated_data):
        user = Usuario(**validated_data)
        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()
        return user

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Usuario
#         fields = ('id', 'username', 'email', 'first_name', 'last_name', 'edad', 'cpf', 'is_active', 'is_staff')
#
#     def update(self, instance, validated_data):
#         instance.username = validated_data.get('username', instance.username)
#         instance.email = validated_data.get('email', instance.email)
#         instance.first_name = validated_data.get('first_name', instance.first_name)
#         instance.last_name = validated_data.get('last_name', instance.last_name)
#         instance.edad = validated_data.get('edad', instance.edad)
#         instance.cpf = validated_data.get('cpf', instance.cpf)
#         instance.is_active = validated_data.get('is_active', instance.is_active)
#         instance.is_staff = validated_data.get('is_staff', instance.is_staff)
#         instance.save()
#         return instance
