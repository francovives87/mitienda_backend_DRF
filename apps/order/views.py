from django.shortcuts import render
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    GenericAPIView,
)
from rest_framework.views import APIView
from .serializers import *
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from apps.tienda.models import Tienda, Plan
from apps.product.models import Product, Variaciones
import json
import datetime
from django.db.models import DateField
from django.db.models.functions import Cast
from django.db.models import Count
from dateutil import parser
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

class CreateAnonymousPersonalData(CreateAPIView):
    serializer_class = AnonymousPersonalDataSerializer


class RegistrarOrden(CreateAPIView):
    serializer_class = ProcesoOrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        print("entro aca?")

        print(request.data)
        serializer = ProcesoOrderSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        tienda_db = Tienda.objects.get(id=serializer.validated_data["tienda"])

        user_personal_data_db = UserPersonalData.objects.get(
            user=self.request.user)

        tienda_request = serializer.validated_data["tienda"]

        # envio instance
        envio_request = serializer.validated_data["envio"]
        print("ENVIO REQUEST")
        print(envio_request)

        if (envio_request == None):
            envio_intance = None
        else:
            envio_request = int(envio_request)
            envio_intance = Envios.objects.get(id=envio_request)
        print("envio_request")
        print(envio_request)
        print("envio_intance")

        print(envio_intance)

        # Ordenes

        plan_search = Tienda.objects.filter(
            id=tienda_request,
        ).values_list('plan', flat=True)

        if plan_search:
            print("plan")
            plan = plan_search[0]
            print(plan)
            plan_db = Plan.objects.get(id=plan)

            print("cantidad de ordenes permitidas")
            cant_orders_allow = plan_db.orders
            print(cant_orders_allow)

            existe_orders = Order.objects.filter(tienda=tienda_request)

            if existe_orders.exists():

                today = datetime.datetime.now()
                mes = today.strftime('%m')

                dic = {
                    "cantidad": 0
                }

                cuento = Order.objects.filter(
                    tienda=tienda_request,
                    created__month=mes,
                ).count()

                cantidad_ordenes_por_mes = int(cuento)

                print("cuenta")
                print(cantidad_ordenes_por_mes)
                print("dateTIME today")
                print(today)
                print("MES")
                print(mes)

                if (cantidad_ordenes_por_mes >= cant_orders_allow):
                    return Response({'msj': "limite excedido"}, status=HTTP_401_UNAUTHORIZED)

        # Ordenes

        orden = Order.objects.create(
            tienda=tienda_db,
            user=self.request.user,
            total=serializer.validated_data["total"],
            metodo_pago=serializer.validated_data["metodo_pago"],
            quantity_products=serializer.validated_data["quantity_products"],
            personal_user_data=user_personal_data_db,
            envio=envio_intance,
        )

        productos = serializer.validated_data["productos"]

        ventas_detalle = []
        variacion_to_save_db = None
        opciones_to_save_db = None
        print("productos")
        print(productos)
        precio = 0
        for prod in productos:
            count = prod["quantity"]
            resta = int(count)
            producto_db = Product.objects.get(id=prod["id"])
            print("prod")
            print(prod)
            if "variacion_id" in prod:
                variacion = Variaciones.objects.get(id=prod["variacion_id"])
                if variacion.no_stock == False:
                    variacion.stock = variacion.stock - resta
                precio = variacion.price
                print(variacion)
                variacion.save()
                variacion_to_save_db = prod["variacion_id"]
            else:
                print("product_db")
                print(producto_db)
                if producto_db.in_offer == True:
                    precio = producto_db.in_offer_price
                    if producto_db.with_stock == True:
                        producto_db.stock = producto_db.stock - resta
                    producto_db.save()
                else:
                    precio = producto_db.price
                    if producto_db.with_stock == True:
                        producto_db.stock = producto_db.stock - resta
                    producto_db.save()
                variacion_to_save_db = None

            if "opciones" in prod:
                opciones_to_save_db = prod["opciones"]
            else:
                opciones_to_save_db = None

            order_detail = Order_detail(
                order=orden,
                product=producto_db,
                quantity=prod["quantity"],
                price_sale=precio,
                price_off=producto_db.in_offer_price,
                variacion_id=variacion_to_save_db,
                options=opciones_to_save_db
            )
            ventas_detalle.append(order_detail)

        orden.save()

        Order_detail.objects.bulk_create(ventas_detalle)

        """ Envio la noticifacion a channel """

        """   res = {"tienda_id": tienda_db.id}
        print(res)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "notifi", {"type": "send_notifi", "text": json.dumps(res)}
        ) """

        dict_res = {"orden_id": orden.id, "mensaje": "OK"}

        return Response(dict_res, status=HTTP_200_OK)


class RegistrarOrdenAnonymous(CreateAPIView):
    serializer_class = ProcesoOrderAnonymousSerializer

    def create(self, request, *args, **kwargs):
        print("entro aca?")

        print(request.data)
        serializer = ProcesoOrderAnonymousSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        tienda_db = Tienda.objects.get(id=serializer.validated_data["tienda"])

        anonymous_user_data_db = AnonymousPersonalData.objects.get(
            id=serializer.validated_data["anonymous_user_data"]
        )

        tienda_request = serializer.validated_data["tienda"]

        # envio instance
        envio_request = serializer.validated_data["envio"]
        print("ENVIO REQUEST")
        print(envio_request)

        if (envio_request == None):
            envio_intance = None
        else:
            envio_request = int(envio_request)
            envio_intance = Envios.objects.get(id=envio_request)
        print("envio_request")
        print(envio_request)
        print("envio_intance")

        print(envio_intance)

        # Ordenes

        plan_search = Tienda.objects.filter(
            id=tienda_request,
        ).values_list('plan', flat=True)

        if plan_search:
            print("plan")
            plan = plan_search[0]
            print(plan)
            plan_db = Plan.objects.get(id=plan)

            print("cantidad de ordenes permitidas")
            cant_orders_allow = plan_db.orders
            print(cant_orders_allow)

            existe_orders = Order.objects.filter(tienda=tienda_request)

            if existe_orders.exists():

                today = datetime.datetime.now()
                mes = today.strftime('%m')

                dic = {
                    "cantidad": 0
                }

                cuento = Order.objects.filter(
                    tienda=tienda_request,
                    created__month=mes,
                ).count()

                cantidad_ordenes_por_mes = int(cuento)

                print("cuenta")
                print(cantidad_ordenes_por_mes)
                print("dateTIME today")
                print(today)
                print("MES")
                print(mes)

                if (cantidad_ordenes_por_mes >= cant_orders_allow):
                    return Response({'msj': "limite excedido"}, status=HTTP_401_UNAUTHORIZED)

        # Ordenes

        orden = Order.objects.create(
            tienda=tienda_db,
            total=serializer.validated_data["total"],
            metodo_pago=serializer.validated_data["metodo_pago"],
            quantity_products=serializer.validated_data["quantity_products"],
            anonymous_user_data=anonymous_user_data_db,
            envio=envio_intance,
        )

        productos = serializer.validated_data["productos"]

        ventas_detalle = []
        variacion_to_save_db = None
        opciones_to_save_db = None
        print("productos")
        print(productos)
        precio = 0
        for prod in productos:
            count = prod["quantity"]
            resta = int(count)
            producto_db = Product.objects.get(id=prod["id"])
            print("prod")
            print(prod)
            if "variacion_id" in prod:
                variacion = Variaciones.objects.get(id=prod["variacion_id"])
                if variacion.no_stock == False:
                    variacion.stock = variacion.stock - resta
                precio = variacion.price
                print(variacion)
                variacion.save()
                variacion_to_save_db = prod["variacion_id"]
            else:
                print("product_db")
                print(producto_db)
                if producto_db.in_offer == True:
                    precio = producto_db.in_offer_price
                    if producto_db.with_stock == True:
                        producto_db.stock = producto_db.stock - resta
                    producto_db.save()
                else:
                    precio = producto_db.price
                    if producto_db.with_stock == True:
                        producto_db.stock = producto_db.stock - resta
                    producto_db.save()
                variacion_to_save_db = None

            if "opciones" in prod:
                opciones_to_save_db = prod["opciones"]
            else:
                opciones_to_save_db = None

            order_detail = Order_detail(
                order=orden,
                product=producto_db,
                quantity=prod["quantity"],
                price_sale=precio,
                price_off=producto_db.in_offer_price,
                variacion_id=variacion_to_save_db,
                options=opciones_to_save_db
            )
            ventas_detalle.append(order_detail)

        orden.save()

        Order_detail.objects.bulk_create(ventas_detalle)

        """ Envio la noticifacion a channel """

        """   res = {"tienda_id": tienda_db.id}
        print(res)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "notifi", {"type": "send_notifi", "text": json.dumps(res)}
        ) """

        dict_res = {"orden_id": orden.id, "mensaje": "OK"}

        return Response(dict_res, status=HTTP_200_OK)


class OrderDetail(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        order = self.request.query_params.get("order", "")
        tienda = self.request.query_params.get("tienda", "")
        return Order.objects.filter(tienda=tienda, id=order)
    

class UniqueDatesListView(ListAPIView):
    serializer_class = DateSerializer  # No necesitamos un serializer para este caso
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        tienda_id = self.request.query_params.get("tienda", "") # Obtén el id de la tienda a filtrar desde la URL
        queryset = Order.objects.filter(tienda_id=tienda_id)
        # Convierte el campo de fecha en un tipo de datos DateField para poder agruparlo
        queryset = queryset.annotate(date=Cast('created', output_field=DateField()))
        # Filtra las fechas duplicadas y ordena de forma descendente
        queryset = queryset.order_by('-date').distinct('date')
        return queryset


class OrdersListDateView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        tienda = self.request.query_params.get("tienda", "") 
        fecha = self.request.query_params.get("fecha", "") 
        
          # Convertimos la fecha string en un objeto de fecha
        if fecha:
            fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d').date()
        else:
            fecha = None
        
         # Filtramos las ordenes por fecha y tienda
        queryset = Order.objects.filter(tienda=tienda)
        if fecha:
            queryset = queryset.filter(created__date=fecha)

        return queryset.order_by('-created')