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
from rest_framework import pagination
from django.db.models.functions import Lower
from .permissions import *
from django.contrib.gis.measure import Distance
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

# Create your views here.



class GeoDjangoStoresNears(ListAPIView):

    serializer_class = GeolocalizationSerializer

    def get_queryset(self):
        lat = self.request.query_params.get("lat", "")
        lng = self.request.query_params.get("lng", "")
        radius = self.request.query_params.get("radius", 5)

        point = Point(float(lng), float(lat))

        return StoreGeo.objects.filter(
            location__distance_lt=(point, Distance(km=radius)),
        ).order_by("-created_at")


#BUSQUEDA TRIAGRAM CATEGORIA DE TIENDA Y GEO
class TiendaSearchByCategorieTrigramGeo(ListAPIView):
    serializer_class = TiendaSerializer

    def get_queryset(self):
        # Obtener parámetros de búsqueda
        categoria = self.request.query_params.get('categoria', '')
        lat = float(self.request.query_params.get('lat', 0))
        lng = float(self.request.query_params.get('lng', 0))

        # Obtener queryset filtrado por categoría y distancia
        queryset = Tienda.objects.annotate(
            similarity=TrigramSimilarity('categories__nombre', categoria),
        ).filter(similarity__gte=0.3)
        if lat and lng:
            user_location = Point(lng, lat, srid=4326)
            queryset = queryset.filter(
                geo_tienda__location__distance_lt=(user_location, Distance(km=5))
            ).order_by('geo_tienda__location')
        return queryset
    
#BUSQUEDA TRIAGRAM POR NOMBRE DE TIENDA Y GEO
class TiendaSearchByNameTrigramGeo(ListAPIView):
    serializer_class = TiendaSerializer

    def get_queryset(self):
        # Obtener parámetros de búsqueda
        tienda = self.request.query_params.get('tienda', '')
        lat = float(self.request.query_params.get('lat', 0))
        lng = float(self.request.query_params.get('lng', 0))

        # Obtener queryset filtrado por categoría y distancia
        queryset = Tienda.objects.annotate(
            similarity=TrigramSimilarity('name', tienda),
        ).filter(similarity__gte=0.3)
        if lat and lng:
            user_location = Point(lng, lat, srid=4326)
            queryset = queryset.filter(
                geo_tienda__location__distance_lt=(user_location, Distance(km=5))
            ).order_by('geo_tienda__location')
        return queryset
    
class TiendaSearchTrigramGeo(ListAPIView):
    serializer_class = TiendaSerializer

    def get_queryset(self):
        # Obtener parámetros de búsqueda
        q = self.request.query_params.get('q', '')
        radius = self.request.query_params.get('radius', 5)
        print(radius)
        lat = float(self.request.query_params.get('lat', 0))
        lng = float(self.request.query_params.get('lng', 0))

        # Obtener queryset filtrado por nombre y distancia
        queryset = Tienda.objects.annotate(
            similarity=TrigramSimilarity('name', q),
        ).filter(similarity__gte=0.3)

        # Si no se encontraron resultados por nombre, buscar por categoría
        if not queryset:
            queryset = Tienda.objects.annotate(
                similarity=TrigramSimilarity('categories__nombre', q),
            ).filter(similarity__gte=0.3)

        # Filtrar por distancia si hay coordenadas
        if lat and lng:
            user_location = Point(lng, lat, srid=4326)
            queryset = queryset.filter(
                geo_tienda__location__distance_lt=(user_location, Distance(km=radius))
            ).order_by('geo_tienda__location')

        return queryset

class CreateTiendaVisitor(APIView):
    serializer_class = TiendaVisitorCreateSerializer

    def post(self, request, *args, **kwargs):

        serializer = TiendaVisitorCreateSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        visitor = serializer.validated_data["visitor"]
        tienda = serializer.validated_data["tienda"]

        print("visitor")
        print(visitor)
        print("tienda")
        print(tienda)

        existe_tiendavisitor = TiendaVisitor.objects.filter(
            visitor=visitor, tienda=tienda
        )
        if existe_tiendavisitor.exists():
            return Response({"msj": "exists"}, status=HTTP_200_OK)
        else:
            TiendaVisitor.objects.create(visitor=visitor, tienda=tienda)
            return Response({"msj": "success"}, status=HTTP_200_OK)
        
class TiendaVisitorListAPIView(ListAPIView):
    serializer_class = TiendaVisitorSerializer

    def get_queryset(self):
        visitor_id = self.request.query_params.get('visitor_id')
        queryset = TiendaVisitor.objects.filter(visitor_id=visitor_id).values('tienda')
        return Tienda.objects.filter(id__in=queryset)
    

#Obtener tiendas cercanas por el id de la categoira:
class GetTiendaByCategorieId(ListAPIView):
    serializer_class = TiendaSerializer

    def get_queryset(self):
        # Obtener parámetros de búsqueda
        categoria_id = self.request.query_params.get('categoria_id', '')
        lat = float(self.request.query_params.get('lat', 0))
        lng = float(self.request.query_params.get('lng', 0))
        radius = int(self.request.query_params.get('radius', 5))  # radius de búsqueda en km

        # Obtener queryset filtrado por categoría y distancia
        queryset = Tienda.objects.all()

        if categoria_id:
            queryset = queryset.filter(categories__id=categoria_id)

        if lat and lng:
            user_location = Point(lng, lat, srid=4326)
            queryset = queryset.filter(
                geo_tienda__location__distance_lt=(user_location, Distance(km=radius))
            ).order_by('geo_tienda__location')

        return queryset