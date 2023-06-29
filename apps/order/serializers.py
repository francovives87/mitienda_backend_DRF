from rest_framework import serializers
from .models import *
from apps.tienda.models import Tienda,Envios
from apps.users.models import User,UserPersonalData
from apps.product.models import Product
import datetime
from babel.dates import format_date
from dateutil import parser


class AnonymousPersonalDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnonymousPersonalData
        fields = ('__all__')


class ProductDetailSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    variacion_id = serializers.IntegerField(required=False)
    opciones = serializers.ListField(required=False)


class ProcesoOrderSerializer(serializers.Serializer):

    tienda = serializers.IntegerField()
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = serializers.CharField()
    quantity_products = serializers.IntegerField(min_value=1)
    productos = ProductDetailSerializer(many=True)
    envio = serializers.CharField(required=False, allow_null=True)


class ProcesoOrderAnonymousSerializer(serializers.Serializer):

    tienda = serializers.IntegerField()
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = serializers.CharField()
    quantity_products = serializers.IntegerField(min_value=1)
    productos = ProductDetailSerializer(many=True)
    anonymous_user_data = serializers.IntegerField()
    envio = serializers.CharField(required=False, allow_null=True)


class TiendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tienda
        fields = (
            'id',
            'name',
            'domain',
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')


class UserDataSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = UserPersonalData
        fields = ('__all__')

class AnonymousUserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnonymousPersonalData
        fields = ('__all__')

class EnviosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Envios
        fields =('__all__')


class ProductInOrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields=(
            'id',
            'title',
            'image',
        )


class OrderProductDetailSerializer(serializers.ModelSerializer):
    product = ProductInOrderDetailSerializer()
    class Meta:
        model = Order_detail
        fields = ('__all__')

class OrderSerializer(serializers.ModelSerializer):

    productos = serializers.SerializerMethodField()
    tienda = TiendaSerializer()
    personal_user_data = UserDataSerializer()
    anonymous_user_data = AnonymousUserDataSerializer()
    envio = EnviosSerializer()

    class Meta:
        model = Order
        fields = (
            'tienda',
            'created',
            'id',
            'user',
            'notas',
            'total',
            'estado',
            'metodo_pago',
            'quantity_products',
            'productos',
            'personal_user_data',
            'visto',
            'mercado_pago_approved',
            'pago',
            'anonymous_user_data',
            'envio',
        )

    def get_productos(self, obj):
        query = Order_detail.objects.filter(order__id=obj.id)
        productos_serializados = OrderProductDetailSerializer(
            query, many=True).data
        return productos_serializados

class DateSerializer(serializers.Serializer):
    original_date = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S.%fZ')
    formatted_date = serializers.DateTimeField(format='%A %d/%m/%Y')

    def to_representation(self, instance):
        # Convierte la fecha y hora en un objeto datetime
        dt = datetime.datetime.combine(instance.date, datetime.time())

        # Utiliza format_date para obtener el nombre del día de la semana en español
        weekday = format_date(dt, "EEEE", locale="es")

        # Crea un diccionario con la representación de la fecha y el nombre del día de la semana
        return {
            'original_date': instance.date,
            'formatted_date': f'{weekday} {instance.date.strftime("%d/%m/%Y")}'
        }
    

