from django.shortcuts import render
from rest_framework import permissions
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.http.response import HttpResponse
from rest_framework import viewsets
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    GenericAPIView,
)

from .serializers import *
from .models import *
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q
from rest_framework import filters
from django.db.models.functions import Greatest
from django.contrib.postgres.search import SearchQuery, SearchRank
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point


# VISTA PARA SERIALIZAR MPTT
class ListCategories(ListAPIView):
    serializer_class = CategorySerializerMPTT

    def get_queryset(self):
        tienda = self.request.query_params.get("tienda", "")
        return Category.objects.filter(
            tienda=tienda,
            level=0
        )


class FeaturedProducts(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        tienda = self.request.query_params.get("tienda", "")
        return Product.objects.filter(
            category__tienda__id=tienda,
            portada=True,
            public=True,
        )


class ProductsOff(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        tienda = self.request.query_params.get("tienda", "")
        return Product.objects.filter(
            category__tienda__id=tienda,
            public=True,
            in_offer=True
        )


class ListProductsNews(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        tienda = self.request.query_params.get("tienda", "")
        return Product.objects.filter(
            category__tienda__id=tienda,
            public=True,
        ).order_by('-created')[:12]


class ProductRetrieveAPIView(RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'id'


class ListAtributosWithItemsOffProduct(ListAPIView):

    serializer_class = AtributosSerializer

    def get_queryset(self):
        product = self.request.query_params.get("product", "")
        return Atributos.objects.filter(
            product=product
        )

class ListProductsOfCategorie(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        category = self.request.query_params.get("category", "")
        tienda = self.request.query_params.get("tienda", "")
        return Product.objects.filter(
            category=category,
            category__tienda = tienda
        )


#BUSQUEDA TRIAGRAM POR TITLE Y DESCRIPTION POR TIENDA
class ProductSearchTrigram(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        search = self.request.query_params.get('search', '')
        tienda = self.request.query_params.get('tienda', '')
        queryset = Product.objects.annotate(
            similarity=Greatest(
                TrigramSimilarity('title', search),
                TrigramSimilarity('description', search),
            ),
        ).filter(
            public=True,
            category__tienda=tienda,  # agregamos el filtro por nombre de tienda
            similarity__gte=0.1,  # umbral de similitud mínimo
        ).order_by('-similarity')
        return queryset
    

#OBTENER LOS PRODUCTOS CERCANOS
class GetProductsNears(ListAPIView):
    serializer_class = PortadaProductSerializer
    
    def get_queryset(self):
        # Obtener latitud y longitud de la ubicación dada
        lat = self.request.query_params.get('lat')
        lng = self.request.query_params.get('lng')
        radius =self.request.query_params.get('radius',5)
        radius=int(radius)
        radius_search= radius * 1000
        print("radius_search")
        print(radius_search)
        # Crear un objeto Point con la latitud y longitud
        pnt = Point(float(lng), float(lat), srid=4326)
        
        # Obtener todos los productos dentro de un radio de 5 km
        queryset = Product.objects.annotate(
            distance=Distance('category__tienda__geo_tienda__location', pnt)
        ).filter(
            Q(category__tienda__geo_tienda__location__distance_lte=(pnt, radius_search))
        ).order_by('-created', 'distance')
        
        return queryset

# BÚSQUEDA DE PRODUCTOS POR SIMILITUD DE TRIGRAMAS Y GEOLOCALIZACIÓN
class ProductSearchGeoTrigram(ListAPIView):
    serializer_class = PortadaProductSerializer

    def get_queryset(self):
        # Obtener los parámetros de consulta
        lat = self.request.query_params.get('lat')
        lng = self.request.query_params.get('lng')
        radius = self.request.query_params.get('radius', 5)
        search = self.request.query_params.get('search', '')

        # Convertir el radio a metros
        radius_meters = float(radius) * 1000

        # Crear un objeto Point con la latitud y longitud proporcionadas
        location = Point(float(lng), float(lat), srid=4326)

        # Obtener todos los productos dentro del radio especificado
        queryset = Product.objects.annotate(
            similarity=Greatest(
                TrigramSimilarity('title', search),
                TrigramSimilarity('description', search),
            ),
            distance=Distance('category__tienda__geo_tienda__location', location)
        ).filter(
            Q(category__tienda__geo_tienda__location__distance_lte=(location, radius_meters)) &
            Q(similarity__gte=0.1)  # Umbral de similitud mínimo
        ).order_by('-created','-similarity')

        return queryset