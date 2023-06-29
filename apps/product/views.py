from django.shortcuts import render
from rest_framework import permissions
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.http.response import HttpResponse
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework import status
from .permissions import isOwner_product, CanCreateMoreImages, CanCreateProduct

from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    GenericAPIView,
)


from .serializers import *

# Create your views here.
######### VISTAS ADMINISTRADOR #####################

# CATEGORIES



# VISTA PARA SERIALIZAR MPTT
class ListCategories(ListAPIView):
    serializer_class = CategorySerializerMPTT
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        tienda = self.request.query_params.get("tienda", "")
        return Category.objects.filter(
            tienda=tienda,
            level=0
            )
    
# lista sin mptt
class ListAllCategories(ListAPIView):
    serializer_class = CategorySerializerList
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        tienda = self.request.query_params.get("tienda", "")
        return Category.objects.filter(
            tienda=tienda
        )
    


class DeleteCategoria(DestroyAPIView):
    serializer_class = CategorySerializer
    """ permission_classes = [permissions.IsAuthenticated,] """
    queryset = Category.objects.all()


class CreateCategorie(CreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated,]


class CategoryDetailView(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = Category.objects.all()
    serializer_class = CategorySerializerNOMPTT


# PRODUCTS

class GetProductsOfCategory(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        kword = self.request.query_params.get("kword", "")
        return Product.objects.filter(
            category=kword,
        )


class GetProductsOfCategoryAdmin(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        categorie = self.request.query_params.get("categorie", "")
        return Product.objects.filter(
            category=categorie,
        )


class CreateProductBasic(CreateAPIView):
    serializer_class = CreateProductBasicSerializer
    permission_classes = [permissions.IsAuthenticated,CanCreateProduct]

class DeleteProduct(DestroyAPIView):
    serializer_class = CreateProductBasicSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Product.objects.all()

class GetImagesOffProduct(ListAPIView):
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        product = self.kwargs.get("product", None)
        return Images.objects.filter(product=product)
    
# Multiple image uploads
def modify_input_for_multiple_files(product, image):
    dict = {}
    dict["product"] = product
    dict["image"] = image
    return dict

    
class CreateMoreProductImages(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [
        permissions.IsAuthenticated,
        CanCreateMoreImages,
    ]

    def get(self, request):
        all_images = Images.objects.all()
        serializer = ImageSerializer(all_images, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, *args, **kwargs):
        product = request.data["product"]


        # converts querydict to original dict
        images = dict((request.data).lists())["image"]
        flag = 1
        arr = []
        for img_name in images:
            modified_data = modify_input_for_multiple_files(product, img_name)
            file_serializer = ImageSerializer(data=modified_data)
            if file_serializer.is_valid():
                file_serializer.save()
                arr.append(file_serializer.data)
            else:
                flag = 0

        if flag == 1:
            return Response(arr, status=status.HTTP_201_CREATED)
        else:
            return Response(arr, status=status.HTTP_400_BAD_REQUEST)
    
class UpadatePortadaStatusProduct(UpdateAPIView):
    serializer_class = UpdatePortadaStatusProduct
    permission_classes = [permissions.IsAuthenticated,]
    queryset = Product.objects.all()

class UpadatePublicStatusProduct(UpdateAPIView):
    serializer_class = UpdatePublicStatusProduct
    permission_classes = [permissions.IsAuthenticated,]
    queryset = Product.objects.all()


    
#####VARIACIONES

##ATRIBUTOS
class ListAtributosWithItemsforProduct(ListAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = AtributosSerializer

    def get_queryset(self):
        product = self.request.query_params.get("product", "")
        return Atributos.objects.filter(
            product = product
        )

class CreateAtributo(CreateAPIView):
    serializer_class = CreateAtributoSerialiezer
    permission_classes = [permissions.IsAuthenticated,]

class DeleteAtributoDelProducto(DestroyAPIView):
    serializer_class = AtributosSerializer
    permission_classes = [permissions.IsAuthenticated,]
    queryset = Atributos.objects.all()

class CreateItemAtributo(CreateAPIView):
    serializer_class = CreateItemAtributoSerializer
    permission_classes = [permissions.IsAuthenticated,]

class UpdateOpciones(UpdateAPIView):
    serializer_class = UpdateOpcionesSerializaer
    permission_classes = [permissions.IsAuthenticated,]
    queryset = Product.objects.all()

##VARIACIONES

class VariacionViewSet(viewsets.ModelViewSet):
    serializer_class = CreateVariacionesSerializer
    permission_classes = [permissions.IsAuthenticated,]
    """ solo permito estos verbos http, porque el delete lo hago aparte por el tema de los permisos """
    http_method_names = ["get", "post", "head"]

    def get_queryset(self):

        variaciones = Variaciones.objects.all()
        return variaciones

class GetVariationsOffProduct(ListAPIView):
    serializer_class = GetVariationsOffProductSerializer

    def get_queryset(self):
        product = self.request.query_params.get("product", "")
        return Variaciones.objects.filter(product=product)

class HasVariationOnlyAttributeUpdate(UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = HasVariationOnlyAttributeSerializer
    queryset = Product.objects.all()

class BuscarVariaciones(GenericAPIView):
    allowed_methods = ["POST"]
    serializer_class = BuscarVariacionesSerializer

    def post(self, request):
        serializer = BuscarVariacionesSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        respuesta = (
            Variaciones.objects.all()
            .filter(
                product=serializer.validated_data["product"],
                item__in=serializer.validated_data["item"],
            )
            .values("pk")
            .annotate(repeticiones=Count("pk"))
        )

        serialized_q = json.dumps(list(respuesta), cls=DjangoJSONEncoder)

        return HttpResponse(serialized_q, content_type="application/json")


class DeleteVariacion(DestroyAPIView):
    serializer_class = CreateVariacionesSerializer
    permission_classes = [permissions.IsAuthenticated,]
    queryset = Variaciones.objects.all()

class UpdateVariacion(UpdateAPIView):
    serializer_class = UpdateVariacionesSerializer
    permission_classes = [permissions.IsAuthenticated,]
    queryset = Variaciones.objects.all()

class ListVariacionEncontrdas(RetrieveAPIView):

    serializer_class = VariacionesSerializer

    def get_queryset(self):
        return Variaciones.objects.all()
    
class GetProductAndVariacionForOrderDetail(ListAPIView):
    serializer_class = ProductAndVariacionesForOrdersSerializer

    def get_queryset(self):
        product = self.request.query_params.get("product", "")
        variation = self.request.query_params.get("variation", "")

        return Variaciones.objects.filter(product=product, id=variation)


######### VISTAS ADMINISTRADOR #####################







