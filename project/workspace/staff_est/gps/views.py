# -*- encoding: utf-8 -*-
from django.shortcuts import render

from django.core import serializers
from djgeojson.serializers import Serializer as GeoJSONSerializer
#from geojson import Point
from django.contrib.gis.geos import Point
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from est.lib import Tiempozona, Rangozona, Listacn , Listatrabajadores, Listaplantas, Posicionestrabajador,Alertatrabajador, testzona
from est.models import Area, Planta, Zona, Trabajador, CentroNegocios,Empresa, TrabajadorDevice
from gps.models import PositionsTraccar, Devices
from itertools import chain
from datetime import datetime
from djgeojson.views import GeoJSONResponseMixin
import json
from django.core.serializers.json import DjangoJSONEncoder
#json.dumps("{}", cls=DjangoJSONEncoder)
from django.core.serializers.python import Serializer
from datetime import timedelta
from django.views.decorators.csrf import ensure_csrf_cookie
# from django_twilio.decorators import twilio_view
# from twilio.twiml import Response
# from twilio.rest import Client
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

import sys

import requests

CONNETCTUS_URL ='https://api.connectus.cl/api_v1/send_sms'
CONNECTUS_ACCOUNT_SID = '9e01f41122384f5ea9192ade9d1c1c0c'
CONNECTUS_AUTH_TOKEN = 'dce7dc65c4bc4d8e829f5a438d54d447'

# TWILIO_ACCOUNT_SID = 'AC73d35e68b6b938c2a53290e610682d33'
# TWILIO_AUTH_TOKEN = '1db8318032ece98e0f64610af655a837'

class FlatJsonSerializer(Serializer):
    def get_dump_object(self, obj):
        data = self._current
        if not self.selected_fields or 'id' in self.selected_fields:
            data['id'] = obj.id
        data['name'] = obj.nombre
        return data

    def end_object(self, obj):
        if not self.first:
            self.stream.write(', ')
        json.dump(self.get_dump_object(obj), self.stream,
                  cls=DjangoJSONEncoder)
        self._current = None

    def start_serialization(self):
        self.stream.write("[")

    def end_serialization(self):
        self.stream.write("]")

    def getvalue(self):
        return super(Serializer, self).getvalue()
#
#class FlatJsonSerializer2(Serializer):
#    def get_dump_object(self, obj):
#        data = self._current
#        if not self.selected_fields or 'id' in self.selected_fields:
#            data['id'] = obj.i
#        data['name'] = obj.nombre
#        data['lat']=obj.lat
#        data['lon']=obj.lon
#        data['apellidop']=obj.apellidop
#        data['apellidon']=obj.apellidom
#        data['i']=obj.id
#        return data
#
#    def end_object(self, obj):
#        if not self.first:
#            self.stream.write(', ')
#        json.dump(self.get_dump_object(obj), self.stream,
#                  cls=DjangoJSONEncoder)
#        self._current = None
#
#    def start_serialization(self):
#        self.stream.write("[")
#
#    def end_serialization(self):
#        self.stream.write("]")
#
#    def getvalue(self):
#        return super(Serializer, self).getvalue()
#
#class FlatJsonSerializer3(Serializer):
#    def get_dump_object(self, obj):
#        data = self._current
#        if not self.selected_fields or 'id' in self.selected_fields:
#            data['id'] = obj.id
#        data['name'] = obj.nombre
#        #data['lat'] = obj.geom.centroid
#        #data['lon'] = obj.geom.centroid
#        return data
#
#    def end_object(self, obj):
#        if not self.first:
#            self.stream.write(', ')
#        json.dump(self.get_dump_object(obj), self.stream,
#                  cls=DjangoJSONEncoder)
#        self._current = None
#
#    def start_serialization(self):
#        self.stream.write("[")
#
#    def end_serialization(self):
#        self.stream.write("]")
#
#    def getvalue(self):
#        return super(Serializer, self).getvalue()
#
#class FlatJsonSerializer4(Serializer):
#    def get_dump_object(self, obj):
#        data = self._current
#        if not self.selected_fields or 'id' in self.selected_fields:
#            data['id'] = obj.id
#        data['name'] = obj.nombre
#        data['lat'] = obj.lat
#        data['lon'] = obj.lon
#        return data
#
#    def end_object(self, obj):
#        if not self.first:
#            self.stream.write(', ')
#        json.dump(self.get_dump_object(obj), self.stream,
#                  cls=DjangoJSONEncoder)
#        self._current = None
#
#    def start_serialization(self):
#        self.stream.write("[")
#
#    def end_serialization(self):
#        self.stream.write("]")
#
#    def getvalue(self):
#        return super(Serializer, self).getvalue()
#
#@ensure_csrf_cookie
##Serialiser copy paste
#class MySerialiser(Serializer):
#    def end_object( self, obj ):
#        self._current['id'] = obj._get_pk_val()
#        self.objects.append( self._current )
#
#
#
#def last_five(request):
##Ultimas 5 posiciones registradas
#    last_five = Positions.objects.order_by('-id')[:5]
#    #serializer = MySerialiser()
#    s = FlatJsonSerializer()
#    #s.serialize(MyModel.objects.all())
#    #data = s.serialize(Positions.objects.order_by('-id')[:5])
#    data = s.serialize(last_five)
#    #data=serializers.serialize('json', last_five, fields=('deviceid','fixtime'))
#    return HttpResponse(data, content_type='application/json')
#
#@ensure_csrf_cookie

def infoplantas(request):
    pl= Planta.objects.all()
    contenidos=[]
#    s = FlatJsonSerializer()
    for p in pl:
        print p.nombre
        contenidos.append(p)
        data = serializers.serialize('json', contenidos)
#       data = serializer.serialize(contenidos)
#    data = s.serialize(contenidos)
#    return HttpResponse(data, content_type='application/json')
    return JsonResponse(contenidos,safe=False)

def planta(request, planta):
#Posiciones registradas dentro de una determinada planta
    pl = Planta.objects.get(nombre = planta)
#    s = FlatJsonSerializer()
    contenidos = []

    for d in Devices.objects.all():
        if(Positions.objects.filter(id = d.positionid).exists()):
            p = Positions.objects.get(id = d.positionid)
            if(pl.geom.contains(p.geom)):
                contenidos.append(p)


#    for p in puntos:
#        if(pl.geom.contains(p.geom)):
#            contenidos.append(p)

#    data = serializers.serialize('json', contenidos)
    data = GeoJSONSerializer().serialize(contenidos, use_natural_keys=True, with_modelname=False)

    return HttpResponse(data)#, content_type='application/json')

def centro(request, planta, centro):

    tcn = Trabajador.objects.filter(centroNegocios__codigo = centro)
#    s = FlatJsonSerializer()
    contenidos = []
    punto=None
    for tr in tcn:
        if tr.gps_id:
#        t = Trabajador.objects.get(id=trabajador) #Trabajadores con el id solicitado
            dev = Devices.objects.get(id=tr.gps_id) #Dispositivo correspondiente al trabajador
            punto = Positions.objects.get(id = dev.positionid)
        auxiliar=Posicionestrabajador()
        auxiliar.lat=punto.lat
        auxiliar.lon=punto.lon
        auxiliar.address=punto.address
        auxiliar.fixtime=punto.fixtime

        auxiliar.nombre=tr.primer_nombre
        auxiliar.apellidop=tr.apellidop
        auxiliar.apellidom=tr.apellidom
        auxiliar.fecha_nac=tr.fecha_nac
        #auxiliar.estudios=t.estudios
        auxiliar.rut=tr.rut
        auxiliar.nivel_riesgo=tr.nivel_riesgo
        auxiliar.direccion=tr.direccion
        #auxiliar.centroNegocios=t.centroNegocios
        #auxiliar.gps=t.gps
        contenidos.append(auxiliar)
#    data = s.serialize(contenidos)
    #data = GeoJSONSerializer().serialize(contenidos, use_natural_keys=True, with_modelname=False)

#    return HttpResponse(data)#, content_type='application/json')
    return JsonResponse(contenidos, safe=False)

def centro2(request, planta, centro):
    #tcn = Trabajador.objects.all()
    tcn = Trabajador.objects.filter(centroNegocios__codigo = centro)
    #s = FlatJsonSerializer()
    contenidos = []
    punto=None
    for i, tr in enumerate(tcn):
        if tr.gps_id:
#        t = Trabajador.objects.get(id=trabajador) #Trabajadores con el id solicitado
            dev = Devices.objects.get(id=tr.gps_id) #Dispositivo correspondiente al trabajador
            punto = Positions.objects.get(id = dev.positionid)
        auxiliar=Alertatrabajador()
        #auxiliar.geom='SRID=4326;POINT()'
        #auxiliar.lat=punto.lat
        #auxiliar.lon=punto.lon
        #auxiliar.address=punto.address
        #auxiliar.fixtime=punto.fixtime
        auxiliar.nombre=tr.primer_nombre+" "+tr.apellidop
        auxiliar.id=tr.id
        auxiliar.i=i
        if(tr.tipo_contacto):
            auxiliar.tipo_contacto=tr.tipo_contacto
        else:
            auxiliar.tipo_contacto="Sin Información"
        if(tr.emergencia):
            auxiliar.nombre_emergencia=tr.emergencia.nombre
            auxiliar.nro_emergencia=tr.emergencia.fono
        else:
            auxiliar.nombre_emergencia="Sin Información"
            auxiliar.nro_emergencia="Sin Información"
        if(tr.foto):
            auxiliar.foto=tr.foto.url
        else:
            auxiliar.foto="/media/avatar/defecto.png"
        #auxiliar.foto=tr.foto.url
        auxiliar.geom=punto.geom
        auxiliar.apellidop=tr.apellidop
        #auxiliar.apellidom=tr.apellidom
        #auxiliar.fecha_nac=tr.fecha_nac
        #auxiliar.estudios=t.estudios
        #auxiliar.rut=tr.rut
        auxiliar.nivel_riesgo=tr.nivel_riesgo
        if(tr.fono):
            auxiliar.fono=tr.fono
        else:
            auxiliar.fono="Sin Información"
        if(tr.cargo):
            auxiliar.cargo=tr.cargo
        else:
            auxiliar.cargo="Sin Información"
        #auxiliar.direccion=tr.direccion
        #auxiliar.centroNegocios=t.centroNegocios
        #auxiliar.gps=t.gps
        contenidos.append(auxiliar)
    #data = s.serialize(contenidos)
    data = GeoJSONSerializer().serialize(contenidos, use_natural_keys=False, with_modelname=False)

    return HttpResponse(data)#, content_type='application/json')

def centro3(request):

    contenidos = []

    for t in Trabajador.objects.all():
        if(TrabajadorDevice.objects.filter(trabajador=t.id).exists()):
            td = TrabajadorDevice.objects.get(trabajador=t.id)
            d = Devices.objects.get(id=td.device_id)
            p = PositionsTraccar.objects.get(id=d.positionid)
            tp = Point(p.longitude, p.latitude)
            foto = None
            if(t.foto):
                foto = t.foto.url
            if(Zona.objects.filter(zona__bbcontains=tp).exists()):
                z =Zona.objects.filter(zona__bbcontains=tp).last().nombre

                if (z != t.last_z):
                    msg = "AVISO: Trabajador %s Ingreso a zona: %s Nivel riesgo: %s Supervisor: %s %s . Monitorear en: http://www.staff.estchile.cl/gps/sms/%s" % (t.nombre, z, t.nivel_riesgo, t.supervisor.nombre, t.supervisor.telefono, td.fono_gps)

                    # client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
                    # client.messages.create(from_="0101010101", to="2323232323", body=msg)
                    # client.messages.create(from_="0101010101", to="2323232323", body=msg)

                    # hasta aqui se ejecuta
                    # sms_twilio_z(msg)

                    # nameFrom = 'Qualitat'
                    numberTo = '+56966967432'

                    # sms = sendSMS(msg, numberTo)

                    # print(msg)

                    # if sms:
                    #     Ok
                    # else:
                    #     No Ok

                    t.last_z = z
                else:
                    print '2'

                    msg = "Msg"
                    sms_twilio_z(msg)

                    
                contenidos.append({ 'nombre': t.nombre,
                                    'geom': tp,
                                    'fono': t.telefono,
                                    'cargo': t.cargo,
                                    'zona': z,
                                    'foto': foto,
                                    'nombre_emergencia': t.emergencia.nombre,
                                    'nro_emergencia': t.emergencia.fono,
                                    'nivel_riesgo': t.nivel_riesgo,
                                    'id': t.id,
                                    'estid': t.estid,
                                    'supervisor': t.supervisor.nombre,
                                    'super_fono': t.supervisor.telefono,
                                    # 'cv': 'cv2',
                                    'fixtime': p.fixtime,
                                  }
                                )
            else:
                contenidos.append({ 'nombre': t.nombre,
                                    'geom': tp,
                                    'fono': t.telefono,
                                    'cargo': t.cargo,
                                    'zona': 'Sin Información',
                                    'foto': foto,
                                    'nombre_emergencia': t.emergencia.nombre,
                                    'nro_emergencia': t.emergencia.fono,
                                    'nivel_riesgo': t.nivel_riesgo,
                                    'id': t.id,
                                    'estid': t.estid,
                                    'supervisor': t.supervisor.nombre,
                                    'super_fono': t.supervisor.telefono,
                                    # 'cv': 'cv1',
                                    'fixtime': p.fixtime,
                                  }
                                )

    data = GeoJSONSerializer().serialize(contenidos, use_natural_keys=False, with_modelname=False)
    return HttpResponse(data)#, content_type='application/json')

def trabajador(request, trabajador):
#Ultima posicion de un trabajador
    contenidos = []
#    s = FlatJsonSerializer()

    t = Trabajador.objects.get(estid=trabajador) #Trabajadores con el id solicitado
    td = TrabajadorDevice.objects.get(trabajador=t.id)
    dev = Devices.objects.get(id=td.device_id) #Dispositivo correspondiente al trabajador
    validos=PositionsTraccar.objects.filter(valid=True)
    punto = validos.get(id=dev.positionid)
    tp = Point(punto.longitude, punto.latitude)

    if( t.salud.exists()):
        salud = t.salud.last().detalle
    else:
        salud = "Sin Informacion"

    if( t.estudios.exists()):
        estudios = t.estudios.last().nombre
    else:
        estudios = "Sin Informacion"

    if( t.capacitacion.exists()):
        capacitacion = t.capacitacion.last().nombre,

    else:
        capacitacion = "Sin Informacion"



    contenidos.append({ 'geom': tp,
                        'lat': punto.latitude,
                        'lon': punto.longitude,
                        'address': punto.address,
                        'fixtime': punto.fixtime,
                        'valid': punto.valid,
                        'primer_nombre': t.primer_nombre,
                        'segundo_nombre': t.segundo_nombre,
                        'apellidop': t.apellidop,
                        'apellidom': t.apellidom,
                        'fecha_nac': t.fecha_nac,
                        'rut': t.rut,
                        'nivel_riesgo': t.nivel_riesgo,
                        'direccion': t.direccion,
                        'deviceid': dev.id,
                        'attributes': punto.attributes,
                        'fono': t.fono,
                        'e_mail': t.e_mail,
                        'emergencia': t.emergencia.nombre,
                        'tipo_contacto': t.tipo_contacto,
                        'centroNegocios': t.centroNegocios.nombre,
                        'cargo': t.cargo,
                        'rol': t.rol.first().nombre,
                        'gps': td.device.name,
                        'supervisor': t.supervisor.primer_nombre+" "+t.supervisor.segundo_nombre,
                        'empresa': t.empresa.nombre,
                        'salud': salud,
                        'estudios': estudios,
                        'capacitacion': capacitacion,
                        'nota': t.nota,
                        'nota2': t.nota2,
                        'id': t.estid,
                       }
                      )

#    contenidos.append(auxiliar)
#    data = s.serialize(contenidos)
    data = GeoJSONSerializer().serialize(contenidos, use_natural_keys=False, with_modelname=False)
    return HttpResponse(data)#, content_type='application/json')

def tiempoplanta(request, planta, fechainicio, fechafin):
#Posiciones registradas en una determinada planta, durante un rango de tiempo (fecha)
#    s = FlatJsonSerializer()
    pl = Planta.objects.get(nombre = planta)

    posiciones = Positions.objects.filter(fixtime__range=[fechainicio,fechafin])
    contenidos = []
    for p in posiciones:
        if(pl.geom.contains(p.geom)):
            contenidos.append(p)
#    data = s.serialize(contenidos)
    #data = GeoJSONSerializer().serialize(contenidos, use_natural_keys=True, with_modelname=False)
#    return HttpResponse(data)
    return JsonResponse(contenidos, safe=False)

def tiempoplantaconhoras(request, planta, fechainicio, fechafin):
#Posiciones registradas en una determinada planta, durante un rango de tiempo (fecha,hora)
    s = FlatJsonSerializer()
    pl = Planta.objects.get(nombre = planta)

    posiciones = Positions.objects.filter(fixtime__range=[fechainicio,fechafin])
    contenidos = []
    for p in posiciones:
        if(pl.geom.contains(p.geom)):
            contenidos.append(p)
    data = s.serialize(contenidos)
    #data = GeoJSONSerializer().serialize(contenidos, use_natural_keys=True, with_modelname=False)
    return HttpResponse(data)

def lugarestrabajador(request, trabajador,planta, fechainicio, fechafin):
#Posiciones de un trabajador de la planta en un rango de tiempo
    s = FlatJsonSerializer()
    pl = Planta.objects.get(nombre = planta)
    fechai = datetime.strptime(fechainicio, '%Y-%m-%d')
    fechaf = datetime.strptime(fechafin, '%Y-%m-%d')

    t = Trabajador.objects.get(id=trabajador) #Trabajadores con el id solicitado
    dev = Devices.objects.get(id=t.gps_id) #Dispositivo correspondiente al trabajador
    posiciones = Positions.objects.filter(fixtime__range=[fechai,fechaf],deviceid=dev)
    contenidos = []
    for p in posiciones:
        if(pl.geom.contains(p.geom)):
            contenidos.append(p)
    data = s.serialize(contenidos)
    #data = GeoJSONSerializer().serialize(contenidos, use_natural_keys=True, with_modelname=False)
    return HttpResponse(data)


def trabajadoresplanta(request, nombreplanta):
#Posiciones de un trabajador de la planta en un rango de tiempo
    s = FlatJsonSerializer()
    contenidos=[]
    emp=Empresa.objects.filter(planta__nombre=nombreplanta)
    tr = Trabajador.objects.filter(empresa=emp) #Trabajadores con el id solicitado
    for t in tr:
        el=Listatrabajadores()
        el.id=t.estid
        el.nombre=t.primer_nombre+" "+t.apellidop+" "+t.apellidom
        contenidos.append(el)
    data = s.serialize(contenidos)
    #data = GeoJSONSerializer().serialize(contenidos, use_natural_keys=True, with_modelname=False)
    return HttpResponse(data)


def listaplantas(request):
#JSON con la lista de las plantas
#    s = FlatJsonSerializer4()
    contenidos=[]
    pl=Planta.objects.all()

#    for i, p in enumerate(pl):
#        el=Listaplantas(i,p.nombre, p.geom.centroid.get_y() , p.geom.centroid.get_x())
#        contenidos.append(el)

    for i, p in enumerate(pl):
        contenidos.append({ 'name': p.nombre,
                            'id': i,
                            'lon':p.geom.centroid.get_x(),
                            'lat':p.geom.centroid.get_y()
                          }
                         )

#    data = s.serialize(contenidos)
#    return HttpResponse(data)
    return JsonResponse(contenidos, safe=False)


def listacentronegocios(request, planta):
#JSON con los centros de negocios de una planta
    s = FlatJsonSerializer()
    contenidos=[]
    if(planta=="Todos"):
        cn=CentroNegocios.objects.all()
        for c in cn:
            el=Listacn()
            el.id=c.codigo
            el.nombre=c.nombre
            contenidos.append(el)
    else:
        pl=Planta.objects.get(nombre=planta)
        cn=CentroNegocios.objects.filter(planta=pl)
        for c in cn:
            el=Listacn()
            el.id=c.codigo
            el.nombre=c.nombre
            contenidos.append(el)
    data = s.serialize(contenidos)
    #data = dos.append(el)
    #GeoJSONSerializer().serialize(contenidos, use_natural_keys=True, with_modelname=False)
    return HttpResponse(data)

#Revisar que nuevo JSON funciona igual
def listatrabajadores(request, cnegocios):
#JSON con los trabajadores de un centro de negocios
#    s = FlatJsonSerializer2()
    contenidos=[]
    i=0
    for t in Trabajador.objects.filter(centroNegocios__codigo = cnegocios):
        if (TrabajadorDevice.objects.filter(trabajador_id=t.id).exists()):
            td = TrabajadorDevice.objects.filter(trabajador_id=t.id).last()
            d = Devices.objects.filter(id=td.device_id).last()
            p = PositionsTraccar.objects.get(id=d.positionid)
            #tp = Point(p.longitude, p.latitude)
            contenidos.append({ 'name': t.primer_nombre+" "+t.apellidop+" "+t.apellidom,
                                'i': t.estid,
                                'id': i,
                                'lon': p.longitude,
                                'lat': p.latitude,
#                                'geom': tp,
                              }
                             )
            i=i+1

    #data = s.serialize(contenidos)
#    data = GeoJSONSerializer().serialize(contenidos, use_natural_keys=True, with_modelname=False)
#    return HttpResponse(data)
    return JsonResponse(contenidos, safe=False)

def zonaplanta(request, planta):
    zonas = Zona.objects.filter(planta__nombre = planta)
    contenidos = []
    for z in zonas:
        contenidos.append({'nombre': z.nombre,'uso': z.uso, 'planta': z.planta.nombre, 'riesgo': z.riesgo, 'geom': z.zona, 'riesgo': z.nivel_riesgo,})

    data = GeoJSONSerializer().serialize(contenidos, use_natural_keys=False, with_modelname=False)
    return HttpResponse(data)

def zonas(request):
    zonas = Zona.objects.all()
    contenidos = []
    for z in zonas:
        contenidos.append({'nombre': z.nombre,'uso': z.uso, 'planta': z.planta.nombre, 'riesgo': z.riesgo, 'geom': z.zona, 'riesgo': z.nivel_riesgo,})

    data = GeoJSONSerializer().serialize(contenidos, use_natural_keys=False, with_modelname=False)
    return HttpResponse(data)



#modificar
def datosinforme(request,cnegocios, trabajador,planta, fechainicio, fechafin):
#Posiciones de un trabajador de la planta en un rango de tiempo
    s = FlatJsonSerializer()
    fechai = datetime.strptime(fechainicio, '%Y-%m-%d')
    fechaf = datetime.strptime(fechafin, '%Y-%m-%d')
    pl = Planta.objects.get(nombre = planta)
    zonas = Zona.objects.filter(planta__nombre=planta)

    t = Trabajador.objects.get(estid=trabajador) #Trabajadores con el id solicitado
    td = TrabajadorDevice.objects.filter(trabajador = t).last()
    dev = Devices.objects.get(id=td.device_id)
#    dev = Devices.objects.get(id=t.gps_id) #Dispositivo correspondiente al trabajador
    #posiciones = Positions.objects.filter(fixtime__range=[fechai,fechaf])
    posiciones = PositionsTraccar.objects.filter(deviceid=dev)
    contenidos = []

    rango=None
    aux1=None
    aux2=None
    aux3=timedelta(microseconds=0)

    for i, z in enumerate(zonas): #Para cada una de las zonas en una planta

        contenidozona=[]
#        tiempozona=Tiempozona(None,None,None,None,None,None,None,None)
#        tiempozona.dif=timedelta(microseconds=0)
        for p in posiciones: #Para cada una de las posiciones
            if((p.fixtime>=fechai)&(p.fixtime<=fechaf) & (p.valid)):

                if(z.zona.contains(Point(p.latitude, p.longitude))): #Si la posicion se encuentra en una zona
                    #contenidozona.append(p) # Creo lista con elementos de una zona, para luego buscar el ultimo y primer registro
                    if not(rango):

                        rango=Rangozona(None,None,None)

                        rango.zona=z
                        rango.fin=p.fixtime
                        aux1=p.fixtime
                        print(aux1)
                        rango.inicio=p.fixtime
                        aux2=p.fixtime
                        print(aux2)
                        #if not(rango.fin):
                            #rango.fin=p.fixtime
                        #if not(rango.inicio):
                            #rango.inicio=p.fixtime
                    else:
                        if(p.fixtime>rango.fin):
                            rango.fin=p.fixtime
                            aux2=p.fixtime
                                #contenidos.append(rango)
                        else:
                            if(rango):


                                rango.aux= aux2 - aux1
                                aux3 =aux3 + aux2 - aux1

                                #contenidos.append(tiempozona)
                                rango=None
                                #total=timedelta(microseconds=0)
                                aux1=None
                                aux2=None


        tiempozona=Tiempozona(None,None,None,None,None,None,None,None)
        tiempozona.nombre=z.nombre
        tiempozona.id=str(aux3)

        contenidos.append(tiempozona)
        aux3=timedelta(microseconds=0)

        #if(contenidozona):
            #pr=contenidozona[0].fixtime
            #ul=contenidozona[-1].fixtime
            #tiempozona=ul-pr
            #obj=Tiempozona()
            #obj.nombre=z.nombre
            #obj.horas=abs(tiempozona.seconds/3600)
            #obj.horas=abs((len(contenidozona)*30)/3600)
            #obj.minutos=abs((tiempozona.seconds - abs(tiempozona.seconds/3600)*3600)/60)

            #obj.minutos=abs((len(contenidozona)*30 - abs(len(contenidozona)*30/3600)*3600)/60)
            #obj.dias=abs(tiempozona.days)
            #obj.primero=pr
            #obj.ultimo=ul
            #contenidos.append(obj)
        #else:
            #obj=Tiempozona()
            #obj.nombre=z.nombre
            #obj.horas=0
            #obj.minutos=0
            #contenidos.append(obj)

    #for i,z in enumerate(zonas):
    #    pr=posicioneszona[i].first().fixtime
    #    ul=posicioneszona[i].last().fixtime
    #    dif=pr-ul
    #    contenidos.append(dif)

    #primero= posiciones.first().fixtime
    #ultimo= posiciones.last().fixtime
    #total=ultimo-primero

    #dias=diferencia.days
    #horas=diferencia.

    data = s.serialize(contenidos)
    #data = serializers.serialize('json', contenidos)
    return HttpResponse(data, content_type='application/json')
#    return JsonResponse(contenidos, safe=False)

def riesgotrabajador(request, planta, nro):
#Posiciones de trabajadores con mayor riesgo
#    s = FlatJsonSerializer()
    pl = Planta.objects.get(nombre = planta)
    empresa= Empresa.objects.get(planta=pl)
    trabs=Trabajador.objects.filter(empresa=empresa)
    tr = trabs.order_by('-nivel_riesgo')[:nro]
    contenidos = []

    for t in tr:
        dev = Devices.objects.get(id=t.gps_id) #Dispositivo correspondiente al trabajador
        punto = Positions.objects.get(id = dev.positionid) #Grupo de puntos relacionados a un trabajador
        if(punto):
            if(pl.geom.contains(punto.geom)):
                auxiliar=Posicionestrabajador()
                auxiliar.lat=punto.lat
                auxiliar.lon=punto.lon
                auxiliar.address=punto.address
                auxiliar.fixtime=punto.fixtime
                auxiliar.fono=t.fono
                auxiliar.nombre=t.primer_nombre
                auxiliar.apellidop=t.apellidop
                auxiliar.apellidom=t.apellidom
                auxiliar.fecha_nac=t.fecha_nac
                #auxiliar.estudios=t.estudios
                auxiliar.rut=t.rut
                auxiliar.nivel_riesgo=t.nivel_riesgo
                auxiliar.direccion=t.direccion
                #auxiliar.centroNegocios=t.centroNegocios
                #auxiliar.gps=t.gps
                contenidos.append(auxiliar)

#    data = s.serialize(contenidos)
    #data = GeoJSONSerializer().serialize(contenidos, use_natural_keys=True, with_modelname=False)
#    return HttpResponse(data)
    return JsonResponse(contenidos,safe=True)


#def curriculum(request, trabajador):
#    s = FlatJsonSerializer()
#    data = Trabajador.objects.get(id=trabajador)
#
#    context = {'data': data}
#
#    return render(request,'cv/cv.html', context)

def sms(request, trabajador):
    td = TrabajadorDevice.objects.get(fono_gps=trabajador)
    t = Trabajador.objects.get(id=td.trabajador_id)
    d = Devices.objects.get(id=td.device_id)
    p = PositionsTraccar.objects.get(id=d.positionid)
    return render(request,'gps/index.html',{
        'nombre':t.primer_nombre,
        'apellidop':t.apellidop,
        'apellidom':t.apellidom,
        'lat':p.latitude,
        'lon':p.longitude,
        'id':t.id,
        'fono':t.fono,
        'cargo':t.cargo,
        'supervisor':t.supervisor.primer_nombre,
        'supervisorp':t.supervisor.apellidop,
        'fono_super': t.supervisor.fono,
        'foto': t.foto.url,
        'hora': p.fixtime,
        'nivel_riesgo': t.nivel_riesgo,
    })

def trabajador_z_riesgo(request, planta):
#    s = FlatJsonSerializer()
    pl = Planta.objects.get(nombre = planta)
    zonas = Zona.objects.filter(planta__nombre=planta)
    empresa= Empresa.objects.get(planta=pl)
    tr=Trabajador.objects.filter(empresa=empresa)
    contenidos=[]

    for i, z in enumerate(zonas): #Para cada una de las zonas en una planta
        for t in tr:
            if(Devices.objects.filter(id=t.gps_id)):
                dev = Devices.objects.get(id=t.gps_id) #Dispositivo correspondiente al trabajador
                punto = Positions.objects.get(id = dev.positionid) #Grupo de puntos relacionados a un trabajador

                if(punto.valid):
                    if(z.zona.contains(punto.geom)):
                        auxiliar=testzona()
                        auxiliar.nombre=t.primer_nombre+" "+t.apellidop
                        auxiliar.zona=z.nombre
                        contenidos.append(auxiliar)
#    data = s.serialize(contenidos)
    #data = GeoJSONSerializer().serialize(contenidos, use_natural_keys=True, with_modelname=False)
#    return HttpResponse(data)
    return JsonResponse(contenidos)

# def sms_nexo(request):
#     return True

@csrf_exempt
def sms_connectus(request):
    # print 'Method: '+request.method

    # print '======='
    data = json.loads(request.body)
    # print data['id_sms']
    # print data['dst_number']
    from_number = data['src_number']
    from_number = from_number.replace('+56', '')
    # print data['src_provider']
    # print data['sms_content']
    # print '======='

    td = TrabajadorDevice.objects.get(fono_gps=from_number)
    t = Trabajador.objects.filter(id=td.trabajador_id).last()
    d = Devices.objects.filter(id=td.device_id).last()
    p = PositionsTraccar.objects.get(id=d.positionid)
    tp = Point(p.longitude, p.latitude)
    if(Zona.objects.filter(zona__bbcontains=Point(p.longitude, p.latitude)).exists()):
        zona =Zona.objects.get(zona__bbcontains=tp).nombre
    else:
        zona = "Sin Informacion"

    # msg = 'Se ha recibido un mensaje SOS dirijase a http://staff.estchile.cl/sms/%s/ para ver las alertas o a http://staff.estchile.cl/est/cv/%s/ para ver su ficha' % (name)

    msg = 'Se ha recibido un mensaje SOS dirijase a http://staff.estchile.cl/sms/3/ para ver las alertas o a http://staff.estchile.cl/est/cv/3/ para ver su ficha.'

    # numberTo = '942144180'
    numberTo=t.supervisor.fono
    sendSMS(msg, numberTo)

    # name = request.POST.get('from', '')

    sendSMS('help me!', from_number)

    return HttpResponse(True)

# @twilio_view
# def sms_twilio(request):
#    name = request.POST.get('from', '')
#    msg = 'Se ha recibido un mensaje SOS dirijase a http://staff.estchile.cl/sms/%s/ para ver las alertas o a http://staff.estchile.cl/est/cv/%s/ para ver su ficha' % (name)
#    r = Response()
#    r.message(msg)
#
#    return r
#
# @twilio_view
# def sms_twilio(request):
#     print('sms_twilio')
# #    from_number = request.POST.get('from', '')
# #    from_number = request.values.get('From', None)
#     client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#     for m in client.messages.list():
#         if(m.to == '2323232323'):
#             from_n = m.from_
#             break
#     from_number = from_n.replace("+56", "")
#
#     td = TrabajadorDevice.objects.get(fono_gps=from_number)
#     t = Trabajador.objects.filter(id=td.trabajador_id).last()
#     d = Devices.objects.filter(id=td.device_id).last()
#     p = PositionsTraccar.objects.get(id=d.positionid)
#     tp = Point(p.longitude, p.latitude)
#     if(Zona.objects.filter(zona__bbcontains=Point(p.longitude, p.latitude)).exists()):
#         zona =Zona.objects.get(zona__bbcontains=tp).nombre
#     else:
#         zona = "Sin Informacion"
#
#     msg = 'SOS: Trabajador: %s %s Zona: %s. Supervisor: %s %s %s. Ingrese a http://cloud1.estchile.cl/gps/sms/%s/ para ver las alertas' % (t.primer_nombre, t.apellidop, zona, t.supervisor.primer_nombre, t.supervisor.apellidop, t.supervisor.fono, from_number)
#     # m = client.messages.create(from_="+56964590932", to="+56999478765", body=msg)
#     m2 = client.messages.create(from_="+56964590932", to="+56950645387", body=msg)
#
#     return m
#
# @twilio_view
# def sms_twilio_z(msg):
#    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#    client.messages.create(from_="0101010101", to="2323232323", body=msg)
#    client.messages.create(from_="+56950645387", to="2323232323", body=msg)
#
#    return m

def sendSMS(msg, numberTo):
    params = dict()
    params['dst_number'] = numberTo
    params['sms_content'] = msg
    response = requests.post(CONNETCTUS_URL, params=params, auth=(CONNECTUS_ACCOUNT_SID, CONNECTUS_AUTH_TOKEN))

    # if !response:
    #     return False

    return True

def adminzonas(request):

    zonas = Zona.objects.all()

    context = {'zonas': zonas}

    return render(request,'zonas/zonas.html', context)

def adminplantas(request):

    plantas = Planta.objects.all()

    context = {'plantas': plantas}

    return render(request,'plantas/plantas.html', context)

def adminareas(request):

    areas = Area.objects.all()

    context = {'areas': areas}

    return render(request,'areas/areas.html', context)

def reportes(request):

    return render(request,'report/report.html')
