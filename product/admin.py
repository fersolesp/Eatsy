from django.contrib import admin
from product.models import Dieta, Producto, UbicacionProducto, Ubicacion

# Register your models here.
admin.site.register(Dieta)
admin.site.register(Producto)
admin.site.register(Ubicacion)
admin.site.register(UbicacionProducto)
