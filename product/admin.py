from django.contrib import admin

from product.models import (Aportacion, CausaReporte,
                            Producto, Reporte, Ubicacion, UbicacionProducto,
                            Valoracion)

class ProductoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'estado']
    list_filter = ['estado']

class ReporteAdmin(admin.ModelAdmin):
    list_display = ['producto', 'causa', 'fecha']
    list_filter = ['causa']

admin.site.register(Producto, ProductoAdmin)
admin.site.register(Ubicacion)
admin.site.register(UbicacionProducto)
admin.site.register(CausaReporte)
admin.site.register(Reporte, ReporteAdmin)
admin.site.register(Valoracion)
admin.site.register(Aportacion)