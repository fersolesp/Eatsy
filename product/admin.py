from django.contrib import admin

from product.models import (Aportacion, CausaReporte, ChangeRequest,
                            Producto, Reporte, Ubicacion, UbicacionProducto,
                            Valoracion)

class ProductoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'estado']
    list_filter = ['estado']

class ReporteAdmin(admin.ModelAdmin):
    list_display = ['producto', 'causa', 'fecha']
    list_filter = ['causa']

class ChangeRequestAdmin(admin.ModelAdmin):
    list_display = ['product', 'creation_user', 'creation_date']

    def apply(modelAdmin, request, queryset):
        for changeRequest in queryset:
            changeRequest.apply()
        
    actions = [apply]


admin.site.register(Producto, ProductoAdmin)
admin.site.register(Ubicacion)
admin.site.register(UbicacionProducto)
admin.site.register(CausaReporte)
admin.site.register(Reporte, ReporteAdmin)
admin.site.register(Valoracion)
admin.site.register(Aportacion)
admin.site.register(ChangeRequest, ChangeRequestAdmin)
