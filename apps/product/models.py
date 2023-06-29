from django.db import models
#Apps terceros
from model_utils.models import TimeStampedModel
##Apps local
from apps.tienda.models import Tienda
from apps.users.models import User
from PIL import Image, ImageDraw, ImageFont
from mptt.models import MPTTModel, TreeForeignKey
from django.conf import settings
from django.utils.text import slugify
from functools import partial
from django.contrib.postgres.search import SearchVectorField,SearchVector
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Concat
from django.db.models import Value



import os

def get_upload_path(instance, filename, field_name):
    tienda_nombre = instance.category.tienda.domain
    product_name = slugify(instance.title)[:50]  # Recorta el nombre a 50 caracteres
    product_name = product_name.replace('_', '-')  # Reemplaza los espacios por guiones bajos
    return os.path.join(tienda_nombre,field_name,product_name,filename)

def get_upload_path_more_images(instance, filename, field_name):
    tienda_nombre = instance.product.category.tienda.domain
    product_name = slugify(instance.product.title)[:50]  # Recorta el nombre a 50 caracteres
    product_name = product_name.replace('_', '-')  # Reemplaza los espacios por guiones bajos
    filename = filename[:50]
    return os.path.join(tienda_nombre,'products',product_name,field_name,filename)

# Create your models here.
class Category(MPTTModel):
    """ Modelo para categorias """
    tienda = models.ForeignKey(
        Tienda,
        verbose_name="category_on_tienda",
        on_delete=models.CASCADE,
        related_name="category_on_tienda"
    )
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    name = models.CharField('Nombre', max_length=40,unique=True)
    image = models.ImageField(
        "Imagen", 
        upload_to="category_product", 
        height_field=None, 
        width_field=None, 
        max_length=None,
        blank=True,
        null=True,
        )
    featured =  models.BooleanField("destacada",default=False)
    

    
    
    def save(self, *args, **kwargs):
        instance = super(Category, self).save(*args, **kwargs)
        if self.image:
            images = Image.open(self.image.path)
            images = images.resize((1024,786))
            images.save(self.image.path,quality=50,optimize=True)
            return instance

    class Meta:
        verbose_name = "Categoria Producto"
        verbose_name_plural = "Categorias Productos"

    def __str__(self):
        return 'tienda_id: '+str(self.tienda.id) + ' tienda_nombre: '+str(self.tienda.name)+' categoria_id: '+str(self.id)+' name: '+str(self.name)

class Product(TimeStampedModel):
    category = models.ForeignKey(
        Category, 
        verbose_name="Categoria", 
        on_delete=models.CASCADE,
        )
    marca = models.CharField("Marca del producto",max_length=100, blank=True,null=True)
    title = models.CharField("Titulo", max_length=200)
    description = models.TextField("Descripcion:")
    public = models.BooleanField("publico",default=False)
    image = models.ImageField(
        "Imagen", 
        upload_to=partial(get_upload_path, field_name='products'),  
        height_field=None, 
        width_field=None, 
        max_length=None,
        null=True,
        blank=True,
        )
    with_price = models.BooleanField("con precio",default=False)
    with_stock= models.BooleanField("with_stock",default=False)
    price = models.DecimalField("Precio", max_digits=10, decimal_places=2, blank=True,null=True)
    portada = models.BooleanField("Destacado",default=False)
    in_offer = models.BooleanField("En oferta",default=False)
    in_offer_price = models.DecimalField("Precio de oferta", max_digits=10, decimal_places=2,null=True,blank=True)
    has_variation = models.BooleanField("Variaciones",default=False)
    has_options = models.BooleanField("con opciones",default=False)
    stock = models.IntegerField("stock",null=True,blank=True)
    type = models.CharField("Tipo", max_length=3, default="pdf")
    visits = models.IntegerField("visitas", default=0)
    # Nuevo campo que combina el título, la descripción y la marca
    similarity = TrigramSimilarity('title', 'description')


    def save(self, *args, **kwargs):
        instance = super(Product, self).save(*args, **kwargs)
        if self.image:
            images = Image.open(self.image.path)
            images = images.resize((640,480))
            images.save(self.image.path,quality=50,optimize=True)
        return instance

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return ' producto_id: ' +  str(self.id)+' producto_nombre: '+ self.title


class Images(TimeStampedModel):
    product= models.ForeignKey(
        Product,
        verbose_name='producto',
        on_delete=models.CASCADE,
        related_name='images_product',
    )
    image = models.ImageField(
        "Image", 
        upload_to=partial(get_upload_path_more_images,field_name='more_images'),
        height_field=None, 
        width_field=None, 
        max_length=None,
        )
    def save(self, *args, **kwargs):
        instance = super(Images, self).save(*args, **kwargs)
        images = Image.open(self.image.path)
        images = images.resize((640,480))
        images.save(self.image.path,quality=50,optimize=True)
        return instance
 
    class Meta:
        verbose_name = "Imagen de producto"
        verbose_name_plural = "Mas Imagenes de los productos"

    def __str__(self):
        return 'product_id: '+ str(self.product.id)+' product_name: '+str(self.product.title)+' image_id: '+str(self.id)  +' image: ' + self.image.url

class Atributos(TimeStampedModel):
    product = models.ForeignKey(
        Product,
        verbose_name="Producto", 
        on_delete=models.CASCADE
    )
    nombre = models.CharField("Nombre",max_length=150)
    repeat= models.IntegerField("Repetir",default=0)
    

    class Meta:
        verbose_name = "Atributo"
        verbose_name_plural = "Atributos"

    def __str__(self):
        return 'product_id :' +str(self.product.id)+' product_name: '+str(self.product.title) + ' atributo_id: '+ str(self.id)+' atributo_name: '+ self.nombre


class Atributos_Items(TimeStampedModel):
    atributo = models.ForeignKey(
        Atributos,
        verbose_name="Atributo", 
        on_delete=models.CASCADE,
        related_name='atributo_item'
    )
    item = models.CharField("Item",max_length=150)

    class Meta:
        verbose_name = "Atributo_Item"
        verbose_name_plural = "Atributos_Items"

    def __str__(self):
        return str(self.atributo.id)+'__'+str(self.atributo.nombre)+'__'+str(self.id)+'__'+ self.item



class Variaciones(TimeStampedModel):
    product = models.ForeignKey(
        Product,
        verbose_name="Producto", 
        on_delete=models.CASCADE
    )
    item = models.ManyToManyField(Atributos_Items)
    stock = models.IntegerField(blank=True,null=True)
    price = models.DecimalField("Precio", max_digits=8, decimal_places=2, blank=True,null=True)
    no_stock = models.BooleanField("no_stock",default=False)
    class Meta:
        verbose_name = "Variacion"
        verbose_name_plural = "Variaciones"

    def __str__(self):
        return 'Id_Producto: '+str(self.product.id)+'__'+' Id_variacion: '+str(self.id)

class OpinionesProducts(TimeStampedModel):
    product = models.ForeignKey(
        Product,
        verbose_name="producto",
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        verbose_name="user",
        on_delete=models.CASCADE
    )
    rating= models.DecimalField("Rating", max_digits=2, decimal_places=1, blank=True,null=True)
    opinion=models.CharField(max_length=255,blank=True,null=True)
    
    class Meta:
        verbose_name = "Opinion Producto"
        verbose_name_plural = "Opiniones Productos"

    def __str__(self):
        return  "opinion_id: "+str(self.id)+" product_id "+ str(self.product.id) + ' product_name ' +str(self.product.title) + ' user '+str(self.user.username)+ ' rating '+str(self.rating)


class PreguntaProduct(TimeStampedModel):
    product = models.ForeignKey(
        Product,
        verbose_name="producto",
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        verbose_name="user",
        on_delete=models.CASCADE
    )
    pregunta = models.CharField(max_length=255,blank=True,null=True)
    respuesta = models.CharField(max_length=255,blank=True,null=True)
    visto = models.BooleanField('visto',default=False)

    

    class Meta:
        verbose_name = "Pregunta a vendedor"
        verbose_name_plural = "Pregunta a vendedor"

    def __str__(self):
        return "id_pregunta" + str(self.id) + " product_id: " +str(self.product.id)+" product_name: "+str(self.product.title) + " user_id :"+ str(self.user.id)+ " username: "+str(self.user.username) +" pregunta: "+str(self.pregunta)


