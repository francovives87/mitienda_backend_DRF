from django.db import models

# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)

from django.db import models
from model_utils.models import TimeStampedModel
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import code_generator

class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(username=username, email=self.normalize_email(email),codregistro=code_generator())
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
                  'twitter': 'twitter', 'email': 'email'}


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))
    codregistro = models.CharField("Codigo_activacion", max_length=9)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email + ' [id_user: ' + str(self.id) +']'

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    
    def credentials(self):
        return {
            'id':str(self.id)
        }
    def get_visitor_id(self, obj):
        visitor = Visitor.objects.filter(user__email=self.email).first()
        if visitor:
            return visitor.id
        return None


class Visitor(TimeStampedModel):
    user = models.ForeignKey(
        User,
        verbose_name='User',
        related_name='user_visitor',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Visitante"
        verbose_name_plural = "Visitantes"

    def __str__(self):
        return 'id_visitor:'+str(self.id)



class UserPersonalData(TimeStampedModel):
    user = models.ForeignKey(
        User,
        related_name='user',
        on_delete=models.CASCADE,
    )
    nombre = models.CharField("Nombre",max_length=50,blank=True,null=True)
    apellido = models.CharField("apellido",max_length=50,blank=True,null=True)
    pais = models.CharField("pais",max_length=50,blank=True,null=True)
    ciudad = models.CharField("ciudad",max_length=50,blank=True,null=True)
    estado = models.CharField("estado/provincia",max_length=50,blank=True,null=True)
    direccion = models.CharField("direccion",max_length=80,blank=True,null=True)
    apartamento = models.CharField("apartamento",max_length=10,blank=True,null=True)
    codigo_postal = models.CharField("codigo postal",max_length=50,blank=True,null=True)
    telefono = models.CharField("telefono",max_length=50,blank=True,null=True)
    dni = models.CharField("dni",max_length=50,blank=True,null=True)

    class Meta:
        verbose_name = "Datos personales"
        verbose_name_plural = "Datos personales"

    def __str__(self):
        return str(self.id)+'_'+ str(self.user.email) + '_' + str(self.nombre) + '_' + str(self.apellido)

