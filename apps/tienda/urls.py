from django import urls
from django.urls import path, re_path
from django.urls.conf import include
from . import views
from . import viewsPublics


urlpatterns = [
    # publica
    path(
        'api/v1.0/tienda/',
        views.GetTiendaByName.as_view(),
        name='GetTiendaByName'
    ),
    path(
        'api/v1/admin/tienda/user/',
        views.GetTiendaByUser.as_view(),
        name='GetTiendaByUser'
    ),

    path('api/categorias/store/cargar/',
         views.CategoryUploadView.as_view(), name='cargar_categorias'),
    path(
        'api/v1/tiendas/categories/list/mptt/',
        views.ListCategoriesTiendas.as_view(),
        name='ListCategories'
    ),

    path('api/v1/tiendas/create/',
         views.TiendaCreateView.as_view(), name='tienda-create'),
    path('tiendas/<int:tienda_id>/add-categorias/',
         views.AddTiendaCategoriaView.as_view(), name='add_tienda_categorias'),
    path(
        'api/v1/tienda/envios/',
        views.GetEnvios.as_view(),
        name='GetEnvios'
    ),
    path(
        'api/v1/tienda/geo/nears/',
        viewsPublics.GeoDjangoStoresNears.as_view(),
        name='GeoDjangoStoresNears'
    ),
    path(
        'api/v1/tienda/search/categories/geo/',
        viewsPublics.TiendaSearchByCategorieTrigramGeo.as_view(),
        name='TiendaSearchByCategorieTrigramGeo'
    ),
    path(
        'api/v1/tienda/search/name/geo/',
        viewsPublics.TiendaSearchByNameTrigramGeo.as_view(),
        name='TiendaSearchByNameTrigramGeo'
    ),
    path(
        'api/v1/tienda/search/store/geo/',
        viewsPublics.TiendaSearchTrigramGeo.as_view(),
        name='TiendaSearchTrigramGeo'
    ),
    path(
        'api/v1/store/visitor/create/',
        viewsPublics.CreateTiendaVisitor.as_view(),
        name='CreateTiendaVisitor'
    ),
    path(
        'api/v1/store/visitor/list/',
        viewsPublics.TiendaVisitorListAPIView.as_view(),
        name='TiendaVisitorListAPIView'
    ),

    path(
        'api/v1/store/by/categories/list/',
        viewsPublics.GetTiendaByCategorieId.as_view(),
        name='GetTiendaByCategorieId'
    ),

    # publica

    # private
    path(
        'api/v1/tienda/user/token/',
        views.GetTiendaByToken.as_view(),
        name='GetTiendaByToken'
    ),
    path(
        'api/v1/admin/tienda/plan/',
        views.GetPlan.as_view(),
        name='GetPlan'
    ),
    path(
        'api/v1/admin/tienda/name/update/<int:pk>',
        views.TiendaNameUpdate.as_view(),
        name='TiendaNameUpdate'
    ),
    path(
        'api/v1/admin/tienda/portada/update/',
        views.TiendaPortadaUpdate.as_view(),
        name='TiendaPortadaUpdate'
    ),
    path(
        'api/v1/admin/tienda/logo/update/',
        views.TiendaLogoUpdate.as_view(),
        name='TiendaLogoUpdate'
    ),
    path(
        'api/v1/admin/tienda/settings/type/<int:pk>/',
        views.UpdateTipoTienda.as_view(),
        name='UpdateTipoTienda'
    ),
    path(
        'api/v1/admin/tienda/settings/payments/methods/<int:pk>/',
        views.UpdateStoreSettingsPaymentsMethods.as_view(),
        name='UpdateStoreSettingsPaymentsMethods'
    ),
    path(
        'api/v1/admin/tienda/settings/orders/recive/<int:pk>/',
        views.UpdateStoreSettingsWpEmailOrders.as_view(),
        name='UpdateStoreSettingsWpEmailOrders'
    ),
    path(
        'api/v1/admin/tienda/settings/orders/wpnumber/<int:pk>/',
        views.UpdateStoreSettingsWpNumber.as_view(),
        name='UpdateStoreSettingsWpNumber'
    ),

    path(
        'api/v1/admin/tienda/envio/create/',
        views.CreateEnvio.as_view(),
        name='CreateEnvio'
    ),
    path(
        'api/v1/admin/tienda/envio/update/<int:pk>/',
        views.UpdateEnvio.as_view(),
        name='UpdateEnvio'
    ),
    path(
        'api/v1/admin/tienda/envio/delete/<int:pk>/',
        views.DeleteEnvio.as_view(),
        name='DeleteEnvio'
    ),
    path(
        'api/v1/admin/tienda/geo/create',
        views.StoreGeoCreateView.as_view(),
        name='StoreGeoCreateView'
    ),



]
