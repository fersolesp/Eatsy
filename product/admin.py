from django.contrib import admin
from product.models import Dieta, Producto, UbicacionProducto, Ubicacion, CausaReporte, Reporte, Aportacion

class ReporteAdmin(admin.ModelAdmin):
    list_display = ['producto', 'fecha', 'causa']
    list_filter = ['causa']

admin.site.register(Dieta)
admin.site.register(Producto)
admin.site.register(Ubicacion)
admin.site.register(UbicacionProducto)
admin.site.register(CausaReporte)
admin.site.register(Reporte, ReporteAdmin)
admin.site.register(Aportacion)