
from django.db.models import fields
from rest_framework import serializers
from .models import User,UserPersonalData,Visitor
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    visitor_id = serializers.IntegerField(required=False)

    default_error_messages = {
        'username': 'The username should only contain alphanumeric characters'}

    class Meta:
        model = User
        fields = ['email', 'username', 'password','visitor_id']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        return attrs

    def create(self, validated_data):
        visitor_id = validated_data.pop('visitor_id', None)
        user = User.objects.create_user(**validated_data)

        if visitor_id is not None:
            visitor = Visitor.objects.filter(id=visitor_id).first()
            if visitor:
                visitor.user = user
                visitor.save()

        return user


class EmailVerificationSerializer(serializers.ModelSerializer):
    codigo = serializers.CharField(max_length=6)
    

    class Meta:
        model = User
        fields = ['codregistro']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(
        max_length=255, min_length=3, read_only=True)

    tokens = serializers.SerializerMethodField()
    credentials = serializers.SerializerMethodField()
    visitor_id = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access'],
        }

    def get_credentials(self,obj):
        user = User.objects.get(email=obj['email'])

        return {
            'cod_ref' : user.credentials()['id'],
        }
    
    def get_visitor_id(self, obj):
        visitor = Visitor.objects.filter(user__email=obj['email']).first()
        if visitor:
            return visitor.id
        return None




    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens', 'credentials', 'visitor_id']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = User.objects.filter(email=email)
        user = auth.authenticate(email=email, password=password)

        if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }



class AdminLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(
        max_length=255, min_length=3, read_only=True)

    tokens = serializers.SerializerMethodField()
    credentials = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access'],
        }

    def get_credentials(self,obj):
        user = User.objects.get(email=obj['email'])

        return {
            'cod_ref' : user.credentials()['id'],
        }

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens','credentials']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = User.objects.filter(email=email)
        user = auth.authenticate(email=email, password=password)

        if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')
        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }

   


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')

class UserDataSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id','username','email','is_staff')

class UserDataPersonalSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserPersonalData
        fields = ('__all__')
        extra_kwargs = {
            'user': {'required': False},
        }

class UpdateUserPersonalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPersonalData
        fields = ('nombre', 'apellido', 'pais', 'ciudad', 'estado', 'direccion', 'apartamento', 'codigo_postal', 'telefono', 'dni')
        extra_kwargs = {
            'user': {'required': False},
        }


class VisitorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Visitor
        fields = ('__all__')

class SetUserOnVisitorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Visitor
        fields= ('user',)

class GetVisitorByUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Visitor
        fields= ('id','user',)


class VisitorManagerSerializer(serializers.Serializer):

    visitor= serializers.IntegerField()


####SERIALIZADOR ENVIO DE EMAIL A @ZIONESTUDIO PARA CONTACTARME

from rest_framework import serializers

class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    lastname = serializers.CharField(max_length=100,required=False)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20,required=False)
    message = serializers.CharField(max_length=500)