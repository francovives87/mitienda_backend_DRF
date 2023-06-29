from model_utils.models import TimeStampedModel
from apps.users.models import User,Visitor
from mptt.models import MPTTModel, TreeForeignKey
from PIL import Image
from django.contrib.gis.db import models
from django.conf import settings
from django.db import transaction
from functools import partial
from PIL import Image, ImageDraw
from io import BytesIO
from django.core.files import File
import qrcode

import os


def get_upload_path(instance, filename, field_name):
    tienda_nombre = instance.tienda.domain
    return os.path.join(tienda_nombre, field_name, filename)


# Create your models here.

class Plan(TimeStampedModel):
    name = models.CharField("Nombre", max_length=50)
    product_products = models.IntegerField("product_products")
    images_x_products = models.IntegerField("imagenes_x_producto")
    images_sliders = models.IntegerField("imagenes_sliders")
    orders = models.IntegerField("ordenes")

    class Meta:
        verbose_name = 'Plan'
        verbose_name_plural = 'Planes'

    def __str__(self):
        return 'id_plan: '+str(self.id)+' nombre: ' + self.name + ' ' + 'product_products' + str(self.product_products) + 'images_x_products' + str(self.images_x_products)


class CategoriaTienda(MPTTModel):
    nombre = models.CharField(max_length=150)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='hijos')

    class MPTTMeta:
        order_insertion_by = ['nombre']

    class Meta:
        verbose_name = 'CategoriaTienda'
        verbose_name_plural = 'CategoriaTiendas'

    def __str__(self):
        return '[ ID ]: '+str(self.id)+' [ NOMBRE ]: '+str(self.nombre)


class Tienda(TimeStampedModel):
    user = models.ForeignKey(
        User,
        verbose_name="User",
        on_delete=models.CASCADE,
    )
    categories = models.ManyToManyField(
        CategoriaTienda,
        verbose_name="CategoriasTienda",
        related_name="Tiendas"
    )
    plan = models.ForeignKey(
        Plan,
        verbose_name="Plan",
        on_delete=models.CASCADE,
        related_name="tienda_plan",
        blank=True,
        null=True
    )
    name = models.CharField('nombre', max_length=150, unique=True)
    domain = models.CharField('dominio', max_length=50, unique=True)
    description = models.CharField('Descripcion', max_length=255)

    def save(self, *args, **kwargs):
        if not self.pk:  # si no tiene un id asignado, significa que es un nuevo objeto
            with transaction.atomic():
                # guarda la instancia de Tienda
                super(Tienda, self).save(*args, **kwargs)
                # crea la instancia de TiendaImages con la tienda asociada
                TiendaImages.objects.create(tienda=self)
                # crea la instancia de Envios con la tienda asociada y datos predefinidos
                Envios.objects.create(
                    tienda=self,
                    name="Retiro en el local",
                    description="Retire el producto en nuestro local",
                    price=0
                )
                # crea la instancia de StoreStatistics con la tienda asociada
                StoreStatistics.objects.create(tienda=self)
                # crea la instancia de Codigo QR con la tienda asociada
                Codigoqr.objects.create(tienda=self)
        else:
            # guarda la instancia de Tienda sin crear una nueva instancia en TiendaImages
            super(Tienda, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Tienda'
        verbose_name_plural = 'Tiendas'

    def __str__(self):
        return '[ ID_TIENDA ]: '+str(self.id)+' [ USER ]: '+str(self.user.email)+' [ NOMBRE ]: ' + self.name + ' [ DOMINIO ]: ' + str(self.domain)


class StoreGeo(models.Model):
    tienda = models.ForeignKey(
        Tienda,
        verbose_name="tienda",
        on_delete=models.CASCADE,
        related_name="geo_tienda"
    )
    house_number = models.CharField(max_length=255, blank=True,null=True)
    road = models.CharField(max_length=255, blank=True,null=True)
    suburb = models.CharField(max_length=255, blank=True,null=True)
    city_district = models.CharField(max_length=255, blank=True,null=True)
    city = models.CharField(max_length=255, blank=True,null=True)
    village = models.CharField(max_length=255, blank=True,null=True)
    municipality = models.CharField(max_length=255, blank=True,null=True)
    region = models.CharField(max_length=255, blank=True,null=True)
    state_district = models.CharField(max_length=255, blank=True,null=True)
    state = models.CharField(max_length=255, blank=True,null=True)
    postcode = models.CharField(max_length=255, blank=True,null=True)
    country = models.CharField(max_length=255, blank=True,null=True)
    location = models.PointField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return  str(self.tienda.name)

    class Meta:
        verbose_name = "Geolozalizacion_geodjango"
        verbose_name_plural = "Geolocalizaciones_geodjango"

    def __str__(self):
        return  str(self.id) + ' ' +str(self.tienda.name)


class Envios(TimeStampedModel):
    tienda = models.ForeignKey(
        Tienda,
        verbose_name="tienda",
        on_delete=models.CASCADE,
        related_name="tienda_envios"
    )
    name = models.CharField("nombre", max_length=100)
    description = models.TextField('description', max_length=255)
    price = models.DecimalField(
        "Precio", max_digits=8, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = "envio"
        verbose_name_plural = "envios"

    def __str__(self):
        return 'tienda_id: '+str(self.tienda.id)+' ' + 'envio_id: '+str(self.id)+' '+'name: '+str(self.name)


class Opiniones(TimeStampedModel):
    tienda = models.ForeignKey(
        Tienda,
        verbose_name="tienda",
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        verbose_name="User",
        on_delete=models.CASCADE
    )
    rating = models.DecimalField(
        "Rating", max_digits=2, decimal_places=1, blank=True, null=True)
    opinion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Opinion"
        verbose_name_plural = "Opiniones"

    def __str__(self):
        return "tienda_id " + str(self.tienda.id) + ' tienda_name ' + str(self.tienda.name) + ' user '+str(self.user.username) + ' rating '+str(self.rating)


class TiendaImages(TimeStampedModel):
    tienda = models.ForeignKey(
        Tienda,
        verbose_name="Tienda",
        on_delete=models.CASCADE,
        related_name="tienda_images"
    )
    logo = models.ImageField(
        "logo",
        upload_to=partial(get_upload_path, field_name='logo'),
        height_field=None,
        width_field=None,
        max_length=None,
        null=True,
        blank=True,
        default='defaults/mitienda_logo_3_2_512.png'
    )
    portada = models.ImageField(
        "portada",
        upload_to=partial(get_upload_path, field_name='portada'),
        height_field=None,
        width_field=None,
        max_length=None,
        null=True,
        blank=True,
        default='defaults/portada1.jpg'
    )

    def save(self, *args, **kwargs):
        instance = super(TiendaImages, self).save(*args, **kwargs)
        if self.logo:
            images = Image.open(self.logo.path)
            images = images.resize((512, 512))
            images.save(self.logo.path, quality=90, optimize=True)
        if self.portada:
            # Abrir la imagen original
            image = Image.open(self.portada.path)

            # Calcular el ancho y alto deseados y la relación de aspecto de la imagen original
            desired_width = 1400
            desired_height = 400
            width, height = image.size
            aspect_ratio = height / width

            # Recortar la imagen en anchura si es necesario
            if aspect_ratio < (desired_height / desired_width):
                new_width = int(height / desired_height * desired_width)
                left = int((width - new_width) / 2)
                right = int((width + new_width) / 2)
                top = 0
                bottom = height
                cropped_image = image.crop((left, top, right, bottom))

            # Recortar la imagen en altura si es necesario
            else:
                new_height = int(width / desired_width * desired_height)
                top = int((height - new_height) / 2)
                bottom = int((height + new_height) / 2)
                left = 0
                right = width
                cropped_image = image.crop((left, top, right, bottom))

            # Sobrescribir la imagen original con el recorte
            os.remove(self.portada.path)
            cropped_image.save(self.portada.path, quality=60, optimize=True)
        return instance

    class Meta:
        verbose_name = "Imagen de la tienda"
        verbose_name_plural = "Imagenes de la tienda"

    def __str__(self):
        return '[ ID ]:' + str(self.id) + ' [TIENDA_ID]: ' + str(self.tienda.id)+' [TIENDA_NOMBRE]: ' + self.tienda.name


class StoreSettings(TimeStampedModel):
    tienda = models.ForeignKey(
        Tienda,
        verbose_name="Tienda",
        on_delete=models.CASCADE,
        related_name="store_settings"
    )
    tipo_tienda = models.CharField(
        "tipo_tienda", max_length=5, default="order")
    only_order = models.BooleanField("solo_ordenar", default=True)
    transfer = models.BooleanField("transferencia", default=False)
    mercadopago = models.BooleanField("mercadopago", default=False)
    order_email = models.BooleanField("orden_email", default=True)
    order_wp = models.BooleanField("orden_wp", default=True)
    wp_number=models.CharField("wp_number",max_length=50,blank=True,null=True)


    class Meta:
        verbose_name = "Configuracion de la tienda"
        verbose_name_plural = "Configuraciones de las tiendas"

    def __str__(self):
        return '[ ID ]:' + str(self.id) + ' [TIENDA_ID]: ' + str(self.tienda.id)+' [TIENDA_NOMBRE]: ' + self.tienda.name


class StoreStatistics(TimeStampedModel):
    tienda = models.ForeignKey(
        Tienda,
        verbose_name="Tienda",
        on_delete=models.CASCADE,
        related_name="store_statistics"
    )
    visits = models.IntegerField("visitas", default=0)
    wp_contacts = models.IntegerField("wp_contactos", default=0)
    wp_products = models.IntegerField("wp_products", default=0)

    class Meta:
        verbose_name = "Estadisticas de la tienda"
        verbose_name_plural = "Estadisticas de las tiendas"

    def __str__(self):
        return str(self.id) + ' ' + str(self.tienda.name)


class Codigoqr(TimeStampedModel):
    tienda = models.ForeignKey(
        Tienda,
        verbose_name="tienda",
        on_delete=models.CASCADE,
        related_name="qr_code"
    )
    qr_code = models.ImageField(upload_to=partial(
        get_upload_path, field_name='qrcode'), blank=True)

    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make('https://mitienda.app/'+self.tienda.domain)
        canvas = Image.new('RGB', (360, 360), 'white')

        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.tienda.domain}'+'.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Codigo QR"
        verbose_name_plural = "Codigos QR"
    
    def __str__(self):
        return  str(self.id) + ' ' +str(self.tienda.name)



class TiendaVisitor(TimeStampedModel):
    tienda = models.ForeignKey(
        Tienda,
        verbose_name="tienda",
        on_delete=models.CASCADE
    )  
    visitor = models.ForeignKey(
        Visitor,
        verbose_name="visitor",
        on_delete=models.CASCADE
    )
    class Meta:
        verbose_name = "TiendaVisitor"
        verbose_name_plural = "TiendaVisitor"
    
    def __str__(self):
        return "id: "+ str(self.id) +"visitor_id:" + str(self.visitor.id)+ " tienda_id: "+str(self.tienda.id) +" tienda_name: "+str(self.tienda.name)

