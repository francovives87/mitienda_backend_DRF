from rest_framework import serializers
from django.db.models import Count, Avg

from .models import (
    Atributos,
    Product,
    Category,
    Atributos_Items,
    Variaciones,
    Images,
    OpinionesProducts,
    PreguntaProduct
)

from apps.product import models
from apps.users.models import User
from apps.tienda.models import Tienda, StoreGeo,TiendaImages


############# SERIALIZADORES ADMIN ##########################

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('__all__')


class CategorySerializerNOMPTT(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'image',)


class CategorySerializerList(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'image']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Elimina el campo parent de la representación
        representation.pop('parent', None)
        return representation


class CategoryNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            'name',
        )


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Images
        fields = ('id', 'product', 'image')

# PRODUCTS


class UpdatePortadaStatusProduct(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('portada',)


class UpdatePublicStatusProduct(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('public',)


class ProductSerializer(serializers.ModelSerializer):
    category = CategoryNameSerializer()
    images_product = ImageSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'category',
            'marca',
            'title',
            'description',
            'public',
            'image',
            'price',
            'portada',
            'in_offer',
            'in_offer_price',
            'has_variation',
            'has_options',
            'stock',
            'with_stock',
            'with_price',
            'images_product',
            'type',
            'visits'
        )


class CreateProductBasicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = (
            'category',
            'marca',
            'title',
            'description',
            'image',
            'type',
            'id',
            'price',
            'in_offer',
            'in_offer_price',
            'with_stock',
            'stock',
            'with_price'
        )


############# SERIALIZADORES ADMIN ##########################


###### SERIALIZADORES PUBLICO ###########

# SERIALIZAR CATEGOGIRAS CON MPTT!!!!!!
class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CategorySerializerMPTT(serializers.ModelSerializer):
    children = RecursiveField(many=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'image', 'children',)


class CategoryNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            'name',
        )


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Images
        fields = ('id', 'product', 'image')


class ProductSerializer(serializers.ModelSerializer):
    category = CategoryNameSerializer()
    images_product = ImageSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'category',
            'marca',
            'title',
            'description',
            'public',
            'image',
            'price',
            'portada',
            'in_offer',
            'in_offer_price',
            'has_variation',
            'has_options',
            'stock',
            'with_stock',
            'with_price',
            'images_product',
            'type',
            'visits'
        )


class PortadaStoreGeoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreGeo
        fields = ("city", "road", "house_number", "village", "municipality",
                  "city_district", "suburb", "region", "state_district", "state", "postcode")


class PortadaTiendaImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TiendaImages
        fields = ("logo",)

class PortadaTiendasSerializer(serializers.ModelSerializer):

    geo_tienda = PortadaStoreGeoSerializer(many=True)
    tienda_images = PortadaTiendaImagesSerializer(many=True)

    class Meta:
        model = Tienda
        fields = ("name", "domain", "geo_tienda","tienda_images")


class PortadaCategoriesSerializer(serializers.ModelSerializer):

    tienda = PortadaTiendasSerializer()

    class Meta:
        model = Category
        fields = (
            'name',
            'tienda',
        )


class PortadaProductSerializer(serializers.ModelSerializer):
    category = PortadaCategoriesSerializer()
    images_product = ImageSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'category',
            'marca',
            'title',
            'description',
            'public',
            'image',
            'price',
            'portada',
            'in_offer',
            'in_offer_price',
            'has_variation',
            'has_options',
            'stock',
            'with_stock',
            'with_price',
            'images_product',
            'type',
            'visits'
        )

# VARIACIONES
# ATRIBUTOS


class CreateItemAtributoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Atributos_Items
        fields = ('__all__')


class Atributos_Items_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Atributos_Items
        fields = (
            'id',
            'item',
        )


class AtributosSerializer(serializers.ModelSerializer):

    atributo_item = Atributos_Items_Serializer(many=True)

    class Meta:
        model = Atributos
        fields = (
            'id',
            'nombre',
            'atributo_item',
            'repeat',
        )


class CreateAtributoSerialiezer(serializers.ModelSerializer):

    class Meta:
        model = Atributos
        fields = ('__all__')


class CreateItemAtributoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Atributos_Items
        fields = ('__all__')


class UpdateOpcionesSerializaer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('has_options',)

# VARIACIONES


class CreateAtributoItemVariacioneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Atributos_Items
        fields = (
            'id',
            'atributo',
            'item',
        )


class GetVariationsOffProductSerializer(serializers.ModelSerializer):

    item = CreateAtributoItemVariacioneSerializer(many=True)

    class Meta:
        model = Variaciones
        fields = (
            'id',
            'product',
            'item',
            'stock',
            'price',
            'no_stock'
        )


class HasVariationOnlyAttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('has_variation',)


class ArrayProductsSerializer(serializers.ListField):

    child = serializers.IntegerField()


class BuscarVariacionesSerializer(serializers.Serializer):

    product = serializers.IntegerField()
    item = ArrayProductsSerializer()


class CreateVariacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variaciones
        fields = (
            'id',
            'product',
            'item',
            'stock',
            'price',
            'no_stock'
        )


class UpdateVariacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variaciones
        fields = (
            'stock',
            'price',
        )


class VariacionesSerializer(serializers.ModelSerializer):

    product = ProductSerializer()
    item = Atributos_Items_Serializer(many=True)

    class Meta:
        model = Variaciones
        fields = (
            'id',
            'product',
            'stock',
            'price',
            'item',
            'no_stock',
        )


class ProductAndVariacionesForOrdersSerializer(serializers.ModelSerializer):

    item = Atributos_Items_Serializer(many=True)

    class Meta:
        model = Variaciones
        fields = (
            'id',
            'product',
            'stock',
            'price',
            'item',
            'no_stock'
        )
