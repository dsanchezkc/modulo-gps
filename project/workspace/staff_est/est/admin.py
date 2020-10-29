from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin

from .models import Area, Planta, CentroNegocios, Trabajador, Riesgo, Zona, Rol, Empresa, Contacto, Salud, Estudios, Capacitacion, TrabajadorDevice, TrabajadorEstudios, TrabajadorCapacitacion

class GpsAdmin(LeafletGeoAdmin):
    settings_overrides = {
        'DEFAULT_CENTER': (-36.8282, -73.0514),
        'DEFAULT_ZOOM': 4,
    }

class CapacitacionInline(admin.TabularInline):
    model = TrabajadorCapacitacion
    extra = 1

class EstudiosInline(admin.TabularInline):
    model = TrabajadorEstudios
    extra = 1

class DevicesInline(admin.TabularInline):
    model = TrabajadorDevice
    extra = 1

class TrabajadorAdmin(admin.ModelAdmin):
    inlines = (CapacitacionInline,EstudiosInline, DevicesInline,)
    ordering = ('-estid',)


admin.site.register(Planta, GpsAdmin)
admin.site.register(CentroNegocios, GpsAdmin)
admin.site.register(Riesgo, GpsAdmin)
admin.site.register(Zona, GpsAdmin)
admin.site.register(Rol)
admin.site.register(Area, GpsAdmin)
admin.site.register(Trabajador, TrabajadorAdmin)
admin.site.register(Empresa)
admin.site.register(Contacto)
admin.site.register(Salud)
admin.site.register(Estudios)
admin.site.register(Capacitacion)
admin.site.register(TrabajadorDevice)
admin.site.register(TrabajadorEstudios)
admin.site.register(TrabajadorCapacitacion)

class ZonaAdmin(admin.ModelAdmin):
    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/gps/adminplantas/')

    def response_change(request, obj):
        return redirect('/gps/adminplantas/')