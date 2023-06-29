from django.urls import path, re_path
from django.urls.conf import include
from . import views
from . import viewPublics
from rest_framework.routers import DefaultRouter

app_name = 'apps.product'


router = DefaultRouter()
router.register('variaciones', views.VariacionViewSet, basename="variaciones")


urlpatterns = [
    #### RUTAS ADMIN#######
    # lista con mptt
    path(
        'api/v1/admin/categories/list/mptt/',
        views.ListCategories.as_view(),
        name='ListCategories'
    ),
    # lista sin mptt
    path(
        'api/v1/admin/categories/list/',
        views.ListAllCategories.as_view(),
        name='ListAllCategories'
    ),

    path(
        'api/v1/admin/categories/delete/<pk>',
        views.DeleteCategoria.as_view(),
        name='DeleteCategoria'
    ),
    path(
        'api/v1/admin/categories/delete/<pk>',
        views.ListAllCategories.as_view(),
        name='ListAllCategories'
    ),
    path(
        'api/v1/admin/categories/create',
        views.CreateCategorie.as_view(),
        name='CreateCategorie'
    ),
    path(
        'api/v1/admin/categories/view/<int:pk>/',
        views.CategoryDetailView.as_view(),
        name='CategoryDetailView'
    ),



    # PRODUCTS
    path(
        'api/v1/admin/categories/product/list/',
        views.GetProductsOfCategoryAdmin.as_view(),
        name='GetProductsOfCategoryAdmin'
    ),
    path(
        'api/v1/admin/product/create',
        views.CreateProductBasic.as_view(),
        name='CreateProductBasic'
    ),

    # VARIACIONES/ATRIBUTOS

    # ATRIBUTOS
    path(
        'api/v1/admin/product/atributos/',
        views.ListAtributosWithItemsforProduct.as_view(),
        name='AdminListAtributosWithItemsforProduct'
    ),
    path(
        'api/v1/admin/product/atributo/create',
        views.CreateAtributo.as_view(),
        name='AdminDeleteAtributo'
    ),

    path(
        'api/v1/admin/product/atributo/item/create',
        views.CreateItemAtributo.as_view(),
        name='AdminCreateItemAtributo'
    ),
    path(
        'api/v1/admin/product/atributo/delete/<pk>/',
        views.DeleteAtributoDelProducto.as_view(),
        name='AdminDeleteAtributo'
    ),
    path(
        'api/v1/admin/product/atributo/update/<int:pk>',
        views.UpdateOpciones.as_view(),
        name='UpdateOpciones'
    ),
    # VARIACIONES

    # lista variaciones por producto
    path(
        'api/v1/admin/product/variation/view/',
        views.GetVariationsOffProduct.as_view(),
        name='AdminCreateItemAtributo'
    ),
    path(
        'api/v1/admin/product/variation/type/update/<pk>',
        views.HasVariationOnlyAttributeUpdate.as_view(),
        name='HasVariationOnlyAttributeUpdate'
    ),
    path(
        'api/v1/admin/product/variations/search/',
        views.BuscarVariaciones.as_view(),
        name='BuscarVariaciones'
    ),
    path(
        'api/v1/admin/variation/delete/<pk>',
        views.DeleteVariacion.as_view(),
        name='DeleteVariacion'
    ),
    path(
        'api/v1/admin/variation/update/<pk>',
        views.UpdateVariacion.as_view(),
        name='UpdateVariacion'
    ),
    path(
        'api/v1/admin/product/variation/<pk>',
        views.ListVariacionEncontrdas.as_view(),
        name='ListVariacionEncontrdas'
    ),
    # variaciones
    path(
        'api/v1/admin/product/images/<int:product>',
        views.GetImagesOffProduct.as_view(),
        name='GetImagesOffProduct'
    ),
    path(
        'api/v1/admin/product/images',
        views.CreateMoreProductImages.as_view(),
        name='CreateMoreProductImages'
    ),
    path(
        'api/v1/admin/product/portada/<int:pk>',
        views.UpadatePortadaStatusProduct.as_view(),
        name='UpadatePortadaStatusProduct'
    ),
    path(
        'api/v1/admin/product/public/<int:pk>',
        views.UpadatePublicStatusProduct.as_view(),
        name='UpadatePublicStatusProduct'
    ),
    path(
        'api/v1/admin/product/delete/<int:pk>',
        views.DeleteProduct.as_view(),
        name='DeleteProduct'
    ),
    path(
        'api/v1/admin/product/variation/detail/',
        views.GetProductAndVariacionForOrderDetail.as_view(),
        name='AdminGetProductAndVariacionForOrderDetail'
    ),

    #### RUTAS ADMIN#######

    #### RUTAS PUBLICAS####
    path(
        'api/v1/categories/list/',
        viewPublics.ListCategories.as_view(),
        name='ListCategories'
    ),
    path(
        'api/v1/category/product/list/',
        views.GetProductsOfCategory.as_view(),
        name='ListProducts'
    ),
    path(
        'api/v1/store/products/featured/',
        viewPublics.FeaturedProducts.as_view(),
        name='FeaturedProducts'
    ),
    path(
        'api/v1/store/products/offs/',
        viewPublics.ProductsOff.as_view(),
        name='ProductsOff'
    ),
    path(
        'api/v1/store/products/news/',
        viewPublics.ListProductsNews.as_view(),
        name='ListProductsNews'
    ),
    path(
        'api/v1/store/products/<int:id>',
        viewPublics.ProductRetrieveAPIView.as_view(),
        name='ProductRetrieveAPIView'
    ),
    path(
        'api/v1/store/product/atributos/',
        viewPublics.ListAtributosWithItemsOffProduct.as_view(),
        name='ListAtributosWithItemsOffProduct'
    ),

    path(
        'api/v1/store/categorie/products/list/',
        viewPublics.ListProductsOfCategorie.as_view(),
        name='ListProductsOfCategorie'
    ),
    path(
        'api/v1/store/product/search/',
        viewPublics.ProductSearchTrigram.as_view(),
        name='ProductSearchTrigram'
    ),
    path(
        'api/v1/products/nears/',
        viewPublics.GetProductsNears.as_view(),
        name='GetProductsNears'
    ),
    path(
        'api/v1/products/search/geo/triagram/',
        viewPublics.ProductSearchGeoTrigram.as_view(),
        name='ProductSearchGeoTrigram'
    ),


    



]
