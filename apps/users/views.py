from django.shortcuts import render
from rest_framework import generics, status, views, permissions
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.views import APIView
from .models import User, UserPersonalData, Visitor
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail, EmailMessage  # funcion para enviar emails
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from django.views.generic import View
from django.http import JsonResponse


# SERIALIZERS
from .serializers import *
# Create your views here.


class TestMail(APIView):
    def get(self, request):
        # send mail
        # envio de email
        codigo = '123'
        user = "franco"
        user_email = 'franco_vives@hotmail.com'
        current_site = 'mitienda.app'
        asunto = 'Confirmacion de Email'
        absurl = 'https://'+current_site+"/api/v1.0/email-verify/?codigo=" + \
            str(codigo)+"&coderef="+str(user)
        mensaje = 'Bienvenido/a a mitienda.app! \n Gracias por registrarse. \n Haga click en el siguiente enlace para verificar su correo electronico: \n' + absurl
        email_remitente = settings.EMAIL_HOST_USER
        #
        send_mail(asunto, mensaje, email_remitente, [user_email])
        # redirigiar a pantalla de validacion de codigo
        return Response({"msj": "ok"}, status=HTTP_200_OK)


class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    """ renderer_classes = (UserRenderer) """
    

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        user = User.objects.get(email=user_data["email"])
        codigo = user.codregistro
        # envio de email

        current_site = get_current_site(request).domain
        url = 'https://mitienda.app/login/'
        asunto = 'Confirmacion de Email'
        absurl = url+"?codigo="+str(codigo)+"&coderef="+str(user.id)
        mensaje = 'Bienvenido/a a mitienda.app! \n Gracias por registrarse. \n Haga click en el siguiente enlace para verificar su correo electronico: \n' + absurl
        email_remitente = settings.EMAIL_HOST_USER
        #
        send_mail(asunto, mensaje, email_remitente, [user.email])
        # redirigiar a pantalla de validacion de codigo

        return Response(user_data, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminLoginAPIView(generics.GenericAPIView):
    serializer_class = AdminLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        codigo = request.GET.get("codigo")
        user_id = request.GET.get("coderef")
        check = User.objects.filter(id=user_id, codregistro=codigo)
        if check:
            check.update(is_verified=True)
            return Response(
                {"message": "Usuario verificado con exito!"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"message": "Algo salio mal"}, status=status.HTTP_400_BAD_REQUEST
            )


class UserData(RetrieveAPIView):
    serializer_class = UserDataSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "id"

    def get_queryset(self):
        id = self.kwargs.get("id", None)
        return User.objects.filter(id=id)


class UserPersonalDataView(APIView):
    serializer_class = UserDataPersonalSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get(self, request):
        user = request.user
        data = UserPersonalData.objects.filter(user=user)[0:1]
        serialize = self.serializer_class(data, many=True)

        return Response(serialize.data, status=status.HTTP_200_OK)


class CreatePersonalDataView(CreateAPIView):
    serializer_class = UserDataPersonalSerializer
    permission_classes = (permissions.IsAuthenticated,)


class PersonaCreateAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        # Comprueba si ya existe un objeto de DatosPersonales para el usuario actual
        personal_data_exists = UserPersonalData.objects.filter(
            user=request.user)

        if personal_data_exists.exists():
            raise ValidationError(
                "Solo se permite un objeto de DatosPersonales por usuario.")
        else:

            serializer = UserDataPersonalSerializer(data=request.data)
            if serializer.is_valid():

                data = {
                    'user': request.user,
                    'nombre': serializer.validated_data.get('nombre'),
                    'apellido': serializer.validated_data.get('apellido'),
                    'pais': serializer.validated_data.get('pais'),
                    'ciudad': serializer.validated_data.get('ciudad'),
                    'estado': serializer.validated_data.get('estado'),
                    'direccion': serializer.validated_data.get('direccion'),
                    'apartamento': serializer.validated_data.get('apartamento'),
                    'codigo_postal': serializer.validated_data.get('codigo_postal'),
                    'telefono': serializer.validated_data.get('telefono'),
                    'dni': serializer.validated_data.get('dni'),
                }

                personal_data = UserPersonalData.objects.create(**data)
                personal_data_serializado = UserDataPersonalSerializer(
                    personal_data)
                return Response(personal_data_serializado.data, status=201)
        return Response(serializer.errors, status=400)


class UserPersonalDataAPIView(UpdateAPIView):
    serializer_class = UpdateUserPersonalDataSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = UserPersonalData.objects.all()



class UpdatePersonalDataView(UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserDataPersonalSerializer
    queryset = UserPersonalData.objects.all()


class CreateVisitor(CreateAPIView):
    serializer_class = VisitorSerializer


class GetVisitor(RetrieveAPIView):
    serializer_class = VisitorSerializer
    queryset = Visitor.objects.all()


class SetUserOnVisitor(UpdateAPIView):
    serializer_class = SetUserOnVisitorSerializer
    queryset = Visitor.objects.all()


class GetVisitorByUser(ListAPIView):
    serializer_class = GetVisitorByUserSerializer

    def get_queryset(self):
        user = self.request.query_params.get("user", "")
        return Visitor.objects.filter(user=user).order_by("-created")


class VisitorManager(APIView):
    serializer_class = VisitorManagerSerializer

    def post(self, request, *args, **kwargs):

        serializer = VisitorManagerSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        visitor_request = int(serializer.validated_data["visitor"])

        print(visitor_request)

        resp = {"status": None, "visitor": None}

        existe_visitor = Visitor.objects.filter(id=visitor_request)

        if existe_visitor.exists():
            resp = {"status": "exists", "visitor": visitor_request}
            return Response(resp, status=HTTP_200_OK)
        else:
            create_visitor = Visitor.objects.create()
            print("create_visitor")
            print(create_visitor.id)
            resp = {"status": "created", "visitor": int(create_visitor.id)}
            return Response(resp, status=HTTP_200_OK)


####ENVIO DE EMAIL A @ZIONESTUDIO PARA CONTACTARME
class ZionEstudioContactView(APIView):
    def post(self, request, format=None):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            # Obtener los datos validados del serializador
            name = serializer.validated_data['name']
            lastname = serializer.validated_data['lastname']
            email = serializer.validated_data['email']
            phone = serializer.validated_data['phone']
            message = serializer.validated_data['message']

            # Crear el contenido del correo electrónico
            subject = 'Nuevo mensaje de contacto'
            body = f'Nombre: {name}\nApellido: {lastname}\nEmail: {email}\nTeléfono: {phone}\nMensaje: {message}'
            from_email = 'contacto@mitienda.app'
            to_email = 'franco@zionestudio.com'

            # Enviar el correo electrónico
            send_mail(subject, body, from_email, [to_email])

            return Response({'message': 'Correo electrónico enviado correctamente.'})
        else:
            return Response(serializer.errors, status=400)
        
class VistaMainJson(View):
    def get(self, request):
        data = {'message': 'mitienda.app Back-end version API 1.0 // Developed by Franco Vives // zionestudio.com'}
        return JsonResponse(data)
