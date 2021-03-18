from django.contrib import admin
from product.models import Producto, UbicacionProducto, Ubicacion

# Register your models here.
admin.site.register(Producto)
admin.site.register(Ubicacion)
admin.site.register(UbicacionProducto)
