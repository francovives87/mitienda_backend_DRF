from rest_framework import permissions
from apps.tienda.models import Tienda, Plan
from django.db.models import Count

class IsMiTienda(permissions.BasePermission):

     def has_permission(self, request, view):
        user = request.user
        tienda_request = 0
        if (request.query_params.get('tienda')):
            tienda_request = request.query_params.get('tienda')
        elif (request.data.get('tienda')):
            tienda_request = request.data.get('tienda')
        elif (view.kwargs.get('pk')):
            tienda_request = view.kwargs.get('pk')
        # uso first  para limpiar el queryset, y traer el valor que necesito limpio unico
        tienda_db = Tienda.objects.filter(
            user=user
        ).first()
        print("tienda request")
        print(tienda_request)
        print("tienda_db")
        print(tienda_db)
        print("tienda_db id")
        print(tienda_db.id)

        if (int(tienda_request) == tienda_db.id):
            return True
        else:
            return False