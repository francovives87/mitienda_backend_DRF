from django.urls import path
from .views import *

urlpatterns = [
    path("api/v1/register/", RegisterView.as_view(), name="register"),
    path("api/v1/login/", LoginAPIView.as_view(), name="login"),
    path("api/v1/email-verify/", VerifyEmail.as_view(), name="email-verify"),
    path("api/v1/user/<int:id>", UserData.as_view(), name="UserData"),
    path(
        "api/v1/user/personal/create/",
        PersonaCreateAPIView.as_view(),
        name="PersonaCreateAPIView",
    ),
    path(
        "api/v1/user/data/personal/",
        UserPersonalDataView.as_view(),
        name="UserPersonalDataView",
    ),
    path(
        "api/v1/user/personal/update/<int:pk>/",
        UserPersonalDataAPIView.as_view(),
        name="UserPersonalDataAPIView",
    ),
    path(
        "api/v1/user/visitor/create/",
        CreateVisitor.as_view(),
        name="CreateVisitor",
    ),
    path(
        "api/v1/user/visitor/<pk>",
        GetVisitor.as_view(),
        name="GetVisitor",
    ),
    path(
        "api/v1/user/visitor/set/<pk>",
        SetUserOnVisitor.as_view(),
        name="SetUserOnVisitor",
    ),

    path(
        "api/v1/user/visitor/get/",
        GetVisitorByUser.as_view(),
        name="GetVisitorByUser",
    ),

    path(
        "api/v1/user/visitor/manager/",
        VisitorManager.as_view(),
        name="VisitorManager",
    ),
    #EMIALS
    #TEST MAIL
    path(
        "api/v1/email/test/",
        TestMail.as_view(),
        name="TestMail",
    ),
    #ENVIO DE EMAIL A @ZIONESTUDIO PARA CONTACTARME
    path(
        "api/v1/contact/zion/email",
        ZionEstudioContactView.as_view(),
        name="ZionEstudioContactView",
    ),
    

]
