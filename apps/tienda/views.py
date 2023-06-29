from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions, generics
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    GenericAPIView,
)
from rest_framework.exceptions import ValidationError
from .serializers import *
from .models import *
from apps.users.models import User
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework import status
from mptt.models import MPTTModel, TreeForeignKey
import xlrd
from rest_framework import pagination
from django.db.models.functions import Lower
from .permissions import *

# Create your views here.


class Pagination200(pagination.PageNumberPagination):
    page_size = 200


class TiendaCreateView(CreateAPIView):
    serializer_class = TiendaCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        wp_number = serializer.validated_data.pop('wp_number', None)
        tienda_instance = serializer.save(user=self.request.user)
        
        if wp_number:
            store_settings = StoreSettings.objects.create(tienda=tienda_instance, wp_number=wp_number)
            store_settings.save()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=HTTP_201_CREATED)



class AddTiendaCategoriaView(APIView):
    def post(self, request, tienda_id):
        try:
            tienda = Tienda.objects.get(id=tienda_id)
        except Tienda.DoesNotExist:
            return Response({'error': f'Tienda con id {tienda_id} no existe'}, status=status.HTTP_404_NOT_FOUND)

        categorias = request.data.get('categorias', [])
        for categoria_id in categorias:
            try:
                categoria = CategoriaTienda.objects.get(id=categoria_id)
            except CategoriaTienda.DoesNotExist:
                return Response({'error': f'Categoría con id {categoria_id} no existe'}, status=status.HTTP_400_BAD_REQUEST)
            tienda.category.add(categoria)

        serializer = TiendaSerializer(tienda)
        return Response(serializer.data, status=status.HTTP_200_OK)


# VISTA PARA SERIALIZAR MPTT
class ListCategoriesTiendas(ListAPIView):
    serializer_class = CategorySerializerMPTT
    pagination_class = Pagination200

    def get_queryset(self):
        tienda = self.request.query_params.get("tienda", "")
        return CategoriaTienda.objects.filter(
            level=0
        ).prefetch_related(
            "hijos"
        ).annotate(
            lower_name=Lower("nombre")
        ).order_by(
            "lower_name"
        )


class CategoryUploadView(APIView):

    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No se proporcionó un archivo.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            wb = xlrd.open_workbook(file_contents=file.read())
            sheet = wb.sheet_by_index(0)
        except:
            return Response({'error': 'No se pudo leer el archivo.'}, status=status.HTTP_400_BAD_REQUEST)

        categories = []
        parent = None

        for i in range(sheet.nrows):
            row = sheet.row_values(i)
            if row[0]:
                parent = CategoriaTienda.objects.create(
                    nombre=row[0].lower(), parent=None)
                categories.append(parent)
            if row[1]:
                child = CategoriaTienda.objects.create(
                    nombre=row[1].lower(), parent=parent)
                categories.append(child)

        return Response({'message': 'Categorías creadas exitosamente.'}, status=status.HTTP_201_CREATED)


class GetTiendaByToken(APIView):
    serializer_class = TiendaSerializerByToken
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        data = Tienda.objects.filter(user=user)[0:1]
        serialize = self.serializer_class(data, many=True)

        return Response(serialize.data, status=status.HTTP_200_OK)


class GetTiendaByName(ListAPIView):
    serializer_class = TiendaSerializer

    def get_queryset(self):
        domain = self.request.query_params.get("domain", "")
        return Tienda.objects.filter(domain=domain)[0:1]


class GetPlan(ListAPIView):
    serializer_class = PlanSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        name = self.request.query_params.get("name", "")
        return Plan.objects.filter(name=name)[0:1]


class GetEnvios(ListAPIView):
    serializer_class = TiendaEnviosSerializar

    def get_queryset(self):
        tienda = self.request.query_params.get("tienda", "")
        return Envios.objects.filter(tienda=tienda)

######################################## VISTAS ADMIN ##############################


class GetTiendaByUser(ListAPIView):
    serializer_class = TiendaSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        user = self.request.query_params.get("user", "")
        return Tienda.objects.filter(user=user)[0:1]


class TiendaNameUpdate(UpdateAPIView):
    serializer_class = TiendaNameEditSerializer
    permission_classes = [permissions.IsAuthenticated, IsMiTienda]
    queryset = Tienda.objects.all()


class TiendaLogoUpdate(APIView):

    permission_classes = [permissions.IsAuthenticated, IsMiTienda]

    def put(self, request):
        tienda = request.data.get('tienda')
        try:
            tienda_image = TiendaImages.objects.get(tienda=tienda)
        except TiendaImages.DoesNotExist:
            return Response(
                {"error": f"No se encontró una imagen para la tienda con ID {tienda}"},
                status=status.HTTP_404_NOT_FOUND
            )

        logo = request.data.get("logo")

        if not logo:
            return Response(
                {"error": "No se proporcionó una imagen para la logo"},
                status=status.HTTP_400_BAD_REQUEST
            )

        tienda_image.logo = logo
        tienda_image.save()

        return Response({"message": f"Portada de la tienda con ID {tienda} actualizada correctamente"})


class TiendaPortadaUpdate(APIView):

    permission_classes = [permissions.IsAuthenticated, IsMiTienda]

    def put(self, request):
        tienda = request.data.get('tienda')
        try:
            tienda_image = TiendaImages.objects.get(tienda=tienda)
        except TiendaImages.DoesNotExist:
            return Response(
                {"error": f"No se encontró una imagen para la tienda con ID {tienda}"},
                status=status.HTTP_404_NOT_FOUND
            )

        portada = request.data.get("portada")

        if not portada:
            return Response(
                {"error": "No se proporcionó una imagen para la portada"},
                status=status.HTTP_400_BAD_REQUEST
            )

        tienda_image.portada = portada
        tienda_image.save()

        return Response({"message": f"Portada de la tienda con ID {tienda} actualizada correctamente"})


class UpdateTipoTienda(UpdateAPIView):
    serializer_class = StoreSettingsUpdateTipoTiendaSerializer
    permission_classes = [permissions.IsAuthenticated,]
    queryset = StoreSettings.objects.all()


class UpdateStoreSettingsPaymentsMethods(UpdateAPIView):
    serializer_class = StoreSettingPaymentsMethodsUpdateSerializer
    permission_classes = [permissions.IsAuthenticated,]
    queryset = StoreSettings.objects.all()

class UpdateStoreSettingsWpEmailOrders(UpdateAPIView):
    serializer_class = StoreSettingsWpEmailOrdersSerializer
    permission_classes = [permissions.IsAuthenticated,]
    queryset = StoreSettings.objects.all()

class UpdateStoreSettingsWpNumber(UpdateAPIView):
    serializer_class = StoreSettingsWpNumber
    permission_classes = [permissions.IsAuthenticated,]
    queryset = StoreSettings.objects.all()


class CreateEnvio(CreateAPIView):
    serializer_class = TiendaEnviosSerializar
    permission_classes = [permissions.IsAuthenticated,]


class UpdateEnvio(UpdateAPIView):
    serializer_class = TiendaEnviosSerializar
    permission_classes = [permissions.IsAuthenticated,]
    queryset = Envios.objects.all()


class DeleteEnvio(DestroyAPIView):
    serializer_class = TiendaEnviosSerializar
    permission_classes = [permissions.IsAuthenticated,]
    queryset = Envios.objects.all()

class StoreGeoCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    def post(self, request):
        tienda_id = request.data.get('tienda')
        try:
            store_geo = StoreGeo.objects.get(tienda_id=tienda_id)
            serializer = GeoDjangoSerializer(store_geo, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except StoreGeo.DoesNotExist:
            serializer = GeoDjangoSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


######################################## VISTAS ADMIN ##############################
