from django.conf.urls import url, patterns
from django.views.generic import TemplateView

from . import views

from djgeojson.views import GeoJSONLayerView

from .models import Positions

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='gps/index2.html'), name='home'),
    url(r'^nuclear/$', TemplateView.as_view(template_name='gps/index42.html'), name='home'),
    url(r'^sms/(?P<trabajador>[\w]+)/$', views.sms, name='home'),
    # url(r'^sms/(?P<numero>[\w]+)/$', views.sms, name='home'),
    url(r'^testzonariesgo/(?P<planta>[\w]+)/$',views.trabajador_z_riesgo, name='planta'),
    url(r'^(?P<planta>[\w]+)/puntos/$',views.planta, name='planta'),
    url(r'^(?P<planta>[\w]+)/(?P<centro>[\w]+)/puntos/$',views.centro, name='centro'),
    # url(r'^(?P<planta>[\w]+)/(?P<centro>[\w]+)/puntos2/$',views.centro2, name='centro'),
    url(r'^puntos3/$',views.centro3, name='centro'),
    url(r'^trabajador/(?P<trabajador>[0-9]+)/$',views.trabajador, name='trabajador'), # Se elimina la palabra "puntos" para evitar procesar consulta anterior
    url(r'^plantas/$',views.listaplantas, name='plantas'),
    url(r'^trabajadores/(?P<cnegocios>[\w]+)/$',views.listatrabajadores, name='trabajadores'),
    url(r'^centrosdenegocio/(?P<planta>[\w]+)/$',views.listacentronegocios, name='cn'),
    url(r'^(?P<nombreplanta>[\w]+)/trabajadores/$',views.trabajadoresplanta, name='trabajadoresplanta'),
    url(r'^(?P<planta>[\w]+)/(?P<fechainicio>(\d{4})[/.-](\d{2})[/.-](\d{2}))/(?P<fechafin>(\d{4})[/.-](\d{2})[/.-](\d{2}))/puntos/$',views.tiempoplanta, name='doc'),
    url(r'^(?P<planta>[\w]+)/(?P<fechainicio>(\d{4})[/.-](\d{2})[/.-](\d{2})[/.\s](\d{2})[/.:](\d{2}))/(?P<fechafin>(\d{4})[/.-](\d{2})[/.-](\d{2})[/.\s](\d{2})[/.:](\d{2}))/puntos/$',views.tiempoplantaconhoras, name='doc'),
    url(r'^(?P<planta>[\w]+)/(?P<trabajador>[\w]+)/(?P<fechainicio>(\d{4})[/.-](\d{2})[/.-](\d{2}))/(?P<fechafin>(\d{4})[/.-](\d{2})[/.-](\d{2}))/$',views.lugarestrabajador, name='centro'),
    url(r'^(?P<planta>[\w]+)/ranking_riesgo/(?P<nro>[0-9]+)/$',views.riesgotrabajador),
    url(r'^plantas.json/$',views.infoplantas),
    url(r'^datosinforme/(?P<planta>[\w]+)/(?P<cnegocios>[\w]+)/(?P<trabajador>[\w]+)/(?P<fechainicio>(\d{4})[/.-](\d{2})[/.-](\d{2}))/(?P<fechafin>(\d{4})[/.-](\d{2})[/.-](\d{2}))/$',views.datosinforme),
    # url(r'^cv/(?P<trabajador>[0-9]+)/$' ,views.curriculum, name='curriculum'),
    # url(r'^smst/$', views.sms_twilio),
    url(r'^smst/$', views.sms_connectus),
    url(r'^zona/(?P<planta>[\w]+)/$', views.zonaplanta),
    url(r'^zonas/$',views.zonas),
    url(r'^adminplantas/$',views.adminplantas),
    url(r'^adminzonas/$',views.adminzonas),
    url(r'^adminareas/$',views.adminareas),
    url(r'^reportes/$',views.reportes),
    url(r'^admin/est/zona/$',views.adminzonas),
    url(r'^admin/est/planta/$',views.adminplantas),
    url(r'^admin/est/area/$',views.adminareas),
]
