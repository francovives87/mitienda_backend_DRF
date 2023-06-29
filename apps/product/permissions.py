from rest_framework import permissions
from apps.tienda.models import Tienda, Plan
from .models import Category, Product, Images, Atributos, Variaciones
from django.db.models import Count


""" LOS IS_HE HAY QUE PONERLOS SIEMPRE QUE EN LOS REQUEST SE ENVIEN EL CAMPO TIENDA!!!,TANTO GET O POST """
""" este para los list, PARA LOS QUE ENVIAR LA TIENDA POR METODO GET """


class IsHe(permissions.BasePermission):

    def has_permission(self, request, view):
        print("====request")
        print(request.user)
        print("request_META")
        print(request.query_params.get('tienda'))

        tienda_db = Tienda.objects.filter(
            user=request.user,
            id=request.query_params.get('tienda')
        )
        print("===tienda_DB")
        print(tienda_db)
        if (tienda_db):
            return True
        else:
            return False


""" ESTE ES PARA LOS RETRIEVE/UPDATE/DELETE, PARA LOS QUE ENVIAN LA TIENDA POR METODO POST """


class IsHe_2(permissions.BasePermission):

    def has_permission(self, request, view):
        print("====IsHE_2")
        print(request.data['tienda'])

        tienda_db = Tienda.objects.filter(
            user=request.user,
            id=request.data['tienda']
        )
        if (tienda_db):
            return True
        else:
            return False


""" EL HAS OBJECT PERMISSION ES PARA LOS RETRIEVE """


class isOwner_category(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        print('ACa que onda?')
        print("queryset")

        tienda = Tienda.objects.get(user=request.user)
        print("user_tienda")
        print(tienda.id)
        category = Category.objects.get(id=obj.id)
        print("categody_db")
        print(category.tienda.id)
        if (category.tienda.id == tienda.id):
            return True
        else:
            return False


class isOwner_product(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        print('ACa que onda?')
        print("queryset")

        tienda = Tienda.objects.get(user=request.user)
        print("user_tienda")
        print(tienda.id)
        product = Product.objects.get(id=obj.id)
        print("categody_db")
        print(product.tienda.id)
        if (product.tienda.id == tienda.id):
            return True
        else:
            return False


class isOwner_image(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        print('ACa que onda?')
        print("queryset")

        # la tienda la saco del user, no hace falta enviarla por axios, muy inteligene!
        tienda = Tienda.objects.get(user=request.user)
        print("user_tienda")
        print(tienda.id)
        images = Images.objects.get(id=obj.id)
        print("categody_db")
        print(images.tienda.id)
        if (images.tienda.id == tienda.id):
            return True
        else:
            return False


class isOwner_atributo(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        print('ACa que onda?')
        print("queryset")

        # la tienda la saco del user, no hace falta enviarla por axios, muy inteligene!
        tienda = Tienda.objects.get(user=request.user)
        print("user_tienda")
        print(tienda.id)
        atributo = Atributos.objects.get(id=obj.id)
        print("atributo")
        print(atributo.product_id)

        product = Product.objects.get(id=atributo.product_id)

        print("producto")
        print(product)

        if (product.tienda.id == tienda.id):
            return True
        else:
            return False


class isOwner_variacion(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        print('ACa que onda?')
        print("queryset")

        # la tienda la saco del user, no hace falta enviarla por axios, muy inteligente!
        tienda = Tienda.objects.get(user=request.user)
        print("user_tienda")
        print(tienda.id)
        variacion = Variaciones.objects.get(id=obj.id)
        print("variacion")
        print(variacion.product_id)

        product = Product.objects.get(id=variacion.product_id)

        print("producto")
        print(product)

        if (product.tienda.id == tienda.id):
            return True
        else:
            return False

# PERMISOS ESPECIALES PARA LA CREACION DE OBJETOS PARA MANEJO CON PLAN
# BASADOS EN IS_HE2, MISMA FUNCION MAS AGREGADO DE CONTAR LA CANTIDAD DE PRODUCTOS
# QUE HAY, Y QUE PUEDE CREER SEGUN SU PLAN.


class CanCreateCategorie(permissions.BasePermission):

    def has_permission(self, request, view):
        print("====IsHE_2")
        print(request.data['tienda'])

        # uso value_list para limpiar el queryset, y traer el valor que necesito limpio
        tienda_db = Tienda.objects.filter(
            user=request.user,
            id=request.data['tienda']
        ).values_list('plan', flat=True)

        if (tienda_db):
            print(tienda_db)
            plan_id = tienda_db[0]
            print(plan_id)

            plan_db = Plan.objects.get(id=plan_id)

            print("cantidad de categorias permitidas")
            cant_categorie_allow = plan_db.product_categories
            print(cant_categorie_allow)

            # existe category

            existe_categoria = Category.objects.filter(
                tienda=request.data['tienda']
            )

            if existe_categoria.exists():

                categories = Category.objects.filter(
                    tienda=request.data['tienda']
                ).values('tienda').annotate(categorias=Count('tienda')).values_list('categorias', flat=True)

                print("Count de categorias creadas")
                cant_categories = categories[0]
                print(cant_categories)
            else:
                cant_categories = 0

            if (cant_categories < cant_categorie_allow):
                return True
            else:
                return False
        else:
            return False


class CanCreateProduct(permissions.BasePermission):

    def has_permission(self, request, view):

        user = request.user

        # uso first  para limpiar el queryset, y traer el valor que necesito limpio unico
        tienda_db = Tienda.objects.filter(
            user=user
        )
        tienda = tienda_db.first()
        tienda_id = tienda.id
        plan_id = tienda.plan.id

        if (tienda_db):
            plan_db = Plan.objects.get(id=plan_id)

            print("cantidad de productos permitidos")
            cant_product_allow = plan_db.product_products
            print(cant_product_allow)

            # existe product?

            existe_products = Product.objects.filter(
                category__tienda__id=tienda_id
            )

            print(existe_products)

            if existe_products.exists():

                cant_products = Product.objects.filter(
                    category__tienda__id=tienda_id
                ).count()

                print("Count de productos creados")
                print(cant_products)
            else:
                cant_products = 0

            if (cant_products < cant_product_allow):
                return True
            else:
                return False
        else:
            return False


class CanCreateMoreImages(permissions.BasePermission):

    def has_permission(self, request, view):
        print("====IsHE_2")
        

        user = request.user

        # uso first  para limpiar el queryset, y traer el valor que necesito limpio unico
        tienda_db = Tienda.objects.filter(
            user=user
        )
        tienda = tienda_db.first()

        # vamos a preguntar si el producto es de esta tienda
        if (not tienda):
            return False
        else:
            tienda_id = tienda.id
            plan_id = tienda.plan.id

            pertenece_producto = Product.objects.filter(
                category__tienda_id = tienda_id
            )
            if not pertenece_producto.exists():
                print(pertenece_producto)
                return False


        if (tienda):
            plan_db = Plan.objects.get(id=plan_id)

            print("cantidad de categorias permitidas")
            cant_images_allow = plan_db.images_x_products
            print(cant_images_allow)

            # primero veo si hay registros

            existe_registro = Images.objects.filter(
                product=request.data['product']
            )

            if existe_registro.exists():

                cant_images_db = Images.objects.filter(
                    product=request.data['product']
                ).values('product').annotate(cantidad=Count('id')).values_list('cantidad', flat=True)
                print("Count de categorias creadas")
                cant_images = cant_images_db[0]
                print(cant_images)
            else:
                cant_images_db = 0
                cant_images = 0

            print(cant_images_db)

            if (cant_images < cant_images_allow):
                return True
            else:
                return False
        else:
            return False
