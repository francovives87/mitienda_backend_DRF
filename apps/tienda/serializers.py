from rest_framework import serializers
from .models import *
from django.db.models import Count, Avg
from apps.product.models import Product, Category
from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import Point
from rest_framework_gis.serializers import GeoModelSerializer


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class StoreSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = StoreSettings
        fields = ('__all__')


class CategorySerializerMPTT(serializers.ModelSerializer):
    hijos = RecursiveField(many=True)

    class Meta:
        model = CategoriaTienda
        fields = ('id', 'nombre', 'hijos',)


class CategoriaTiendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaTienda
        fields = ('id', 'nombre')


class TiendaImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = TiendaImages
        fields = ('portada', 'logo',)


class TiendaCodigoQr(serializers.ModelSerializer):

    class Meta:
        model = Codigoqr
        fields = ("qr_code",)


class PlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plan
        fields = ('__all__')


class StoreSettingsUpdateTipoTiendaSerializer(serializers.ModelSerializer):

    class Meta:
        model = StoreSettings
        fields = ('tipo_tienda',)


class StoreSettingPaymentsMethodsUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = StoreSettings
        fields = ('only_order', 'transfer', 'mercadopago',)


class StoreSettingsWpEmailOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreSettings
        fields = ('order_email', 'order_wp',)


class StoreSettingsWpNumber(serializers.ModelSerializer):
    class Meta:
        model = StoreSettings
        fields = ('wp_number',)


class TiendaCreateSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        many=True, queryset=CategoriaTienda.objects.all())
    wp_number = serializers.CharField(write_only=True, allow_blank=True, allow_null=True)

    class Meta:
        model = Tienda
        fields = ['name', 'domain', 'description',
                  'user', 'categories', 'id', 'plan','wp_number']
        read_only_fields = ['user']


class TiendaNameEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tienda
        fields = ('name',)


class TiendaEnviosSerializar(serializers.ModelSerializer):

    class Meta:
        model = Envios
        fields = ('__all__')


class GeoDjangoSerializer(GeoModelSerializer):
    class Meta:
        model = StoreGeo
        geo_field = "location"
        fields = "__all__"


class TiendaSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()
    average = serializers.SerializerMethodField('get_average_field')
    tienda_images = TiendaImagesSerializer(many=True)
    store_settings = StoreSettingsSerializer(many=True)
    qr_code = TiendaCodigoQr(many=True)
    geo_tienda = GeoDjangoSerializer(many=True)

    def get_average_field(self, id):
        return Opiniones.objects.filter(
            tienda=id
        ).aggregate((Avg('rating')))

    class Meta:
        model = Tienda
        fields = ('id', 'name', 'domain', 'categories',
                  'description', 'average', 'tienda_images', 'store_settings', 'qr_code', "geo_tienda")

    def get_categories(self, obj):
        return CategoriaTiendaSerializer(obj.categories.all(), many=True).data


class TiendaSerializerByToken(serializers.ModelSerializer):

    plan = PlanSerializer()
    total_products = serializers.SerializerMethodField()
    store_settings = StoreSettingsSerializer(many=True)
    geo_tienda = GeoDjangoSerializer(many=True)

    class Meta:
        model = Tienda
        fields = ('id', 'name', 'domain', 'plan',
                  'total_products', 'store_settings', 'geo_tienda')

    def get_total_products(self, obj):
        return Product.objects.filter(category__tienda=obj).count()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['total_products'] = self.get_total_products(instance)
        return representation


class TiendaSerializerToSeachrs(serializers.ModelSerializer):

    categories = serializers.SerializerMethodField()
    average = serializers.SerializerMethodField('get_average_field')
    tienda_images = TiendaImagesSerializer(many=True)

    def get_categories(self, obj):
        return CategoriaTiendaSerializer(obj.categories.all()[:3], many=True).data

    def get_average_field(self, id):
        return Opiniones.objects.filter(
            tienda=id
        ).aggregate(Avg('rating'))

    class Meta:
        model = Tienda
        fields = (
            "name",
            "domain",
            "description",
            "average",
            "tienda_images",
            "categories"
        )


class GeolocalizationSerializer(GeoModelSerializer):

    tienda = TiendaSerializerToSeachrs()

    class Meta:
        model = StoreGeo
        geo_field = "location"
        fields = ('tienda', 'city', 'village', 'road',
                  'house_number', 'municipality', 'state_district')


class TiendaVisitorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TiendaVisitor
        fields = "__all__"


class TiendaVisitorSerializer(serializers.ModelSerializer):

    tienda_images = TiendaImagesSerializer(many=True)

    def get_average_field(self, id):
        return Opiniones.objects.filter(
            tienda=id
        ).aggregate((Avg('rating')))

    class Meta:
        model = Tienda
        fields = ('id', 'name', 'domain',
                  'description', 'tienda_images',)
