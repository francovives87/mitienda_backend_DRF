from django.db import models
from django.db.models.fields import DecimalField, PositiveIntegerField
from django.db.models.fields.related import ForeignKey
from model_utils.models import TimeStampedModel
from django.contrib.postgres.fields import ArrayField
from apps.tienda.models import Tienda,Envios,StoreSettings
from apps.users.models import User,UserPersonalData
from apps.product.models import Product
from django.core.mail import send_mail
from django.conf import settings



# Create your models here.
class AnonymousPersonalData(TimeStampedModel):
    nombre = models.CharField("Nombre",max_length=50)
    apellido = models.CharField("apellido",max_length=50)
    email = models.CharField("email",max_length=100,blank=True,null=True)
    pais = models.CharField("pais",max_length=50,blank=True,null=True)
    ciudad = models.CharField("ciudad",max_length=50,blank=True,null=True)
    estado = models.CharField("estado/provincia",max_length=50,blank=True,null=True)
    direccion = models.CharField("direccion",max_length=80)
    apartamento = models.CharField("apartamento",max_length=10,blank=True,null=True)
    codigo_postal = models.CharField("codigo postal",max_length=50,blank=True,null=True)
    telefono = models.CharField("telefono",max_length=50)
    dni = models.CharField("telefono",max_length=50,blank=True,null=True)


    class Meta:
        verbose_name = "anonymous user data"
        verbose_name_plural = "anonymous user data"

    def __str__(self):
        return str(self.id)+'_'+ str(self.email) + '_' + self.nombre + '_' + self.apellido
    




class Order(TimeStampedModel):
    tienda = models.ForeignKey(
        Tienda,
        verbose_name="Tienda",
        on_delete=models.CASCADE
    )
    user = ForeignKey(
        User,
        related_name='Usuario',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    personal_user_data = models.ForeignKey(
        UserPersonalData,
        verbose_name="Datos Personales",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    anonymous_user_data = models.ForeignKey(
        AnonymousPersonalData,
        verbose_name="anonymous_user_data",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    envio = models.ForeignKey(
        Envios,
        verbose_name="Envio",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    notas = models.CharField("Notas",blank=True,null=True,max_length=255)
    total = models.DecimalField("Total",max_digits=10,decimal_places=2)
    estado = models.CharField("estado",max_length=20,default="en espera")
    metodo_pago = models.CharField("Metodo de pago",max_length=20,default="efectivo")
    quantity_products = PositiveIntegerField('cantidad de productos')
    visto = models.BooleanField('visto',default=False)
    mercado_pago_approved=models.BooleanField('mercado_pago_approved',default=False)
    pago=models.CharField('pago',max_length=11,default='pendiente')

    def save(self, *args, **kwargs):
    # Envía el correo electrónico solo si es una nueva orden
        if not self.pk:
            #creo instancia orden y guardo
            super().save(*args, **kwargs)
        # Obtener la instancia de StoreSettings para la tienda actual
            store_settings = self.tienda.store_settings.first()

            #compruebo si el dueño de la tienda, tiene notifiaciones por mail activada.
            if store_settings and store_settings.order_email:

                store_owner_email = self.tienda.user.email

                # Componer el asunto del correo electrónico
                subject = f'Nueva orden en {self.tienda.name}'

                # Componer el cuerpo del correo electrónico
                message = f'Se ha recibido una nueva orden en {self.tienda.name}. ID de la orden: {self.pk}. \n Total: {self.total} \n Cantidad de productos: {self.quantity_products} \n Metodo de pago: {self.metodo_pago}. \n LiNK PARA VER LA ORDEN: https://mitienda.app/admin/orders?order_id={self.id}'

                # Enviar el correo electrónico
                email_host_user = settings.EMAIL_HOST_USER
                default_from_email = settings.DEFAULT_FROM_EMAIL
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=default_from_email,
                    recipient_list=[store_owner_email],
                    fail_silently=False,
                )
            #Envio email al comprador siempre, tanto sea user o anonimo
            # Componer el asunto del correo electrónico
            if self.personal_user_data:
                subject = f'Nueva orden en {self.tienda.name}'

                # Componer el cuerpo del correo electrónico
                message = f'Se ha recibido una nueva orden en {self.tienda.name}. ID de la orden: {self.pk}. \n Total: {self.total} \n Cantidad de productos: {self.quantity_products} \n Metodo de pago: {self.metodo_pago}. \n LiNK PARA VER LA ORDEN: https://mitienda.app/admin/orders?order_id={self.id}'
                if self.user:
                    buyer_email = self.user.email
                elif self.anonymous_user_data:
                    buyer_email = self.anonymous_user_data.email
                else:
                    buyer_email = None

                message = f"Muchas Gracias por realizar su orden en nuesta tienda! \n El ID de la orden es #{self.pk} \n {self.tienda.name}" 
                default_from_email = settings.DEFAULT_FROM_EMAIL
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=default_from_email,
                    recipient_list=[buyer_email],
                    fail_silently=False,
                )

    class Meta: 
        verbose_name = "Orden"
        verbose_name_plural = "Ordenes"

    def __str__(self):
        return 'tienda_id: ' + str(self.tienda.id)+' tienda_name: '+str(self.tienda.name)+' Orden_id_ '+str(self.id)

class Order_detail(TimeStampedModel):
    order = ForeignKey(
        Order,
        related_name="Orden",
        on_delete=models.CASCADE,
    )
    product = ForeignKey(
        Product,
        related_name="Producto",
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField('cantidad')
    price_sale = models.DecimalField("Precion_venta",max_digits=10,decimal_places=2)
    price_off =  models.DecimalField("Precion_en_oferta",max_digits=10,decimal_places=2,blank=True,null=True)
    variacion_id = models.IntegerField("Variacion_id",null=True,blank=True)
    options = ArrayField(
        models.CharField("opciones", max_length=255), blank=True, null=True
    )

    class Meta:
        verbose_name = "Orden Detalle"
        verbose_name_plural = "Ordenes Detalles"

    def __str__(self):
        return str(self.order.id) + '_' + str(self.product.title)