from django.urls import path, re_path
from .views import *

urlpatterns = [
    path(
        "api/v1/user/data/anonymous/create",
        CreateAnonymousPersonalData.as_view(),
        name="CreateAnonymousPersonalData",
    ),
    path(
        "api/v1/tienda/order/user/create",
        RegistrarOrden.as_view(),
        name="RegistrarOrden",
    ),
    path(
        "api/v1/tienda/order/anonymous/create",
        RegistrarOrdenAnonymous.as_view(),
        name="RegistrarOrdenAnonymous",
    ),
    
    ###ADMIN

    path(
        "api/v1/admin/order/view",
        OrderDetail.as_view(),
        name="OrderDetail",
    ),
    path(
        "api/v1/admin/order/dates/",
        UniqueDatesListView.as_view(),
        name="UniqueDatesListView",
    ),
    path(
        "api/v1/admin/order/dates/list/",
        OrdersListDateView.as_view(),
        name="OrdersListDateView",
    ),    
]
