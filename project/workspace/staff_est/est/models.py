from __future__ import unicode_literals

from django.contrib.gis.db import models

from gps.models import Devices

import qrcode
import StringIO

from django.core.urlresolvers import reverse  
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import redirect
from smart_selects.db_fields import ChainedForeignKey

#from qrcode.image.pure import PymagingImage

class EmpresaMandante (models.Model):
    razon_social = models.CharField(max_length=128)
    rut = models.CharField(max_length=128)
    contacto = models.CharField(max_length=128,blank=True, null=True)
    class Meta:
       managed = False
       db_table = 'empresa_mandantes'
    def __unicode__(self):
        return u"%s" % (self.razon_social )




class Contacto (models.Model):
    nombre = models.CharField(max_length=128)
    fono = models.CharField(max_length=128,blank=True, null=True)
    e_mail = models.CharField(max_length=256, blank=True, null=True)
    nota = models.CharField(max_length=128, blank= True, null=True)

    def __unicode__(self):
        return u"%s %s %s" % (self.nombre, self.nota, self.fono)


class Empresa (models.Model):
    nombre = models.CharField(max_length=128, blank=True, null=True)
    rut = models.CharField(max_length=128, blank=True, null=True)
    contacto = models.ForeignKey(Contacto, blank=True, null=True)

    def __unicode__(self):
        return u"%s" % (self.nombre)


class Planta(models.Model):
    nombre = models.CharField(max_length=128, blank=True, null=True)
    empresa = models.ForeignKey(EmpresaMandante, blank=True, null=True)
    geom = models.MultiPolygonField(srid=4326, blank=True, null=True)

    objects = models.GeoManager()
    def response_add(self, request, obj, post_url_continue=None):
        return redirect('http://staff.estchile.cl/gps/adminplantas/')

    def response_change(self, request, obj):
        return redirect('http://staff.estchile.cl/gps/adminplantas/')
    def __unicode__(self):
        return u"%s " % (self.nombre)

class Contrato (models.Model):
    nombre = models.CharField(max_length=128)
    empresa_mandante = models.ForeignKey(EmpresaMandante, blank=True, null=True)
    class Meta:
       managed = False
       db_table = 'contratos'
    def __unicode__(self):
        return u"%s" % (self.nombre )

class Riesgo(models.Model):
    nombre = models.CharField(max_length=128, blank=True, null=True)
    tipo = models.CharField(max_length=128, blank=True, null=True)

    def __unicode__(self):
        return u"%s" % (self.nombre)


class Zona(models.Model):
    nombre = models.CharField(max_length=128, blank=True, null=True)
    uso = models.CharField(max_length=128, blank=True, null=True)
    empresa_mandante= models.ForeignKey(EmpresaMandante, blank=True, null=True)
    contrato  = ChainedForeignKey(
        Contrato, "empresa_mandante","empresa_mandante"
        )
    riesgo = models.ManyToManyField(Riesgo, blank=True, null=True)
    zona = models.MultiPolygonField(srid=4326)
    nivel_riesgo = models.IntegerField(blank=True, null=True)
    def response_add(self, request, obj, post_url_continue=None):
        return HttpResponseRedirect(reverse("admin:otherappname_modelname_changelist"))

    def response_change(self, request, obj):
        return HttpResponseRedirect(reverse("admin:otherappname_modelname_changelist"))
    def __unicode__(self):
        return u"%s" % (self.nombre)


class CentroNegocios(models.Model):
    nombre = models.CharField(max_length=128, blank=True, null=True)
    planta = models.ForeignKey(Planta, blank=True, null=True)
    codigo = models.CharField(max_length=24, blank=True, null=True)
    zonas = models.ManyToManyField(Zona, blank=True, null=True)
    
    def __unicode__(self):
        return u"%s %s" % (self.codigo, self.nombre)


class Rol(models.Model):
    nombre = models.CharField(max_length=128, blank=True, null=True)
    zonas_permitidas = models.ManyToManyField(Zona, blank=True, null=True)

    def __unicode__(self):
        return u"%s" % (self.nombre)


class Salud(models.Model):
    SALUD_CHOICES = (
        ('ALERGIA','Alergia'),
        ('ENFERMEDAD','Enfermedad'),
    )

    DETALLE_CHOICES = (
        ('PENICILINA','Penicilina'),
        ('POLVO','Polvo'),
        ('CIRROSIS','Cirrosis'),
        ('DIABETES','Diabetes'),
        ('CHOCOLATE','Chocolate'),
    )

    tipo = models.CharField(max_length=128, blank=True, null=True, choices=SALUD_CHOICES)
    detalle = models.CharField(max_length=128, blank=True, null=True)#, choices=DETALLE_CHOICES)
    observacion = models.CharField(max_length=2048, blank=True, null=True)

    def __unicode__(self):
        return u"%s %s" % (self.tipo, self.detalle)

class Area (models.Model):
    nombre = models.CharField(max_length=128)
    
    empresa= models.ForeignKey(EmpresaMandante, blank=True, null=True)
    contrato  = ChainedForeignKey(
        Contrato, "empresa_mandante","empresa_mandante"
        )
    geom = models.MultiPolygonField(srid=4326, blank=True, null=True)
    class Meta:
       managed = False
       db_table = 'area'
    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/gps/adminareas')

    def response_change(self, request, obj):
        return redirect('/gps/adminareas')
    def __unicode__(self):
        return u"%s" % (self.nombre )

class Estudios(models.Model):
    nombre = models.CharField(max_length=512, blank=True, null=True)
    establecimiento = models.CharField(max_length=512, blank=True, null=True)
#    fecha = models.DateField(blank=True, null=True)
#    observacion = models.CharField(max_length=4096, blank=True, null=True)
   
    def __unicode__(self):
        return u"%s %s" % (self.nombre, self.establecimiento)

class Capacitacion(models.Model):
    MODALIDAD_CHOICES = (
        ('PRESENCIAL','Presencial'),
        ('ON LINE','On Line'),
        ('MIXTO','Mixto')
    )

    nombre = models.CharField(max_length=512, blank=True, null=True)
    establecimiento = models.CharField(max_length=512, blank=True, null=True)
#    fecha = models.DateField(blank=True, null=True)
#    observacion = models.CharField(max_length=4096, blank=True, null=True)
    modalidad = models.CharField(max_length=128, blank=True, null=True, choices=MODALIDAD_CHOICES)
    horas = models.IntegerField(blank=True, null=True)
    
    def __unicode__(self):
        return u"%s %s" % (self.nombre, self.establecimiento)


class Trabajador(models.Model):
    
    TIPO_CONTACTO_CHOICES = (
        ('PADRE','Padre'),
        ('MADRE','Madre'),
        ('ESPOSO','Esposa(o)'),
        ('ABUELO','Abuelo(a)'),
        ('HIJO','Hijo(a)'),
        ('PAREJA','Pareja'),
        ('POLOLO','Pololo(a)')
    )
    
    estid = models.IntegerField(blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)
#    segundo_nombre = models.CharField(max_length=128, blank=True, null=True)
#    apellidop = models.CharField(max_length=128, blank=True, null=True)
#    apellidom = models.CharField(max_length=128, blank=True, null=True)
    foto = models.ImageField(upload_to='avatar/', blank=True, null=True)
    fecha_nac = models.DateField(blank=True, null=True)
    edad = models.IntegerField(blank=True, null=True)
    direccion = models.CharField(max_length=256, blank=True, null=True)
#    contacto = models.ForeignKey(Contacto, blank=True, null=True)
    telefono = models.IntegerField(blank=True, null=True)
    e_mail = models.CharField(max_length=128, blank=True, null=True)
    emergencia = models.ForeignKey(Contacto, blank=True, null=True)
    tipo_contacto = models.CharField(max_length=128, blank=True, null=True, choices=TIPO_CONTACTO_CHOICES)
    rut = models.CharField(max_length=128, blank=True, null=True)
    centronegocios = models.ForeignKey(CentroNegocios, blank=True, null=True)
    cargo = models.CharField(max_length=128, blank=True, null=True)
    rol = models.ManyToManyField(Rol, blank=True, null=True)
#    gps = models.ForeignKey(Devices, blank=True, null=True)
    gps = models.ManyToManyField(Devices, blank=True, null=True, through='TrabajadorDevice')
    supervisor = models.ForeignKey('Trabajador', blank=True, null=True)
    empresa = models.ForeignKey(Empresa, blank=True, null=True)
    salud = models.ManyToManyField(Salud, blank=True, null=True)
    estudios = models.ManyToManyField(Estudios, blank=True, null=True, through='TrabajadorEstudios')      
    capacitacion = models.ManyToManyField(Capacitacion, blank=True, null=True, through='TrabajadorCapacitacion')
    nivel_riesgo = models.IntegerField(blank=True, null=True)
    nota = models.CharField(max_length=256, blank=True, null=True)
    nota2 = models.CharField(max_length=256, blank=True, null=True)
    qrtext = models.CharField(max_length=256, blank=True, null=True)
    qrimg = models.ImageField(upload_to='qr/', blank=True, null=True)
    last_z = models.CharField(max_length=128, blank=True, null=True)


#    def save(self, *args, **kwargs):
#        self.qrtext = "http://www.estchile.cl/cv/"+str(self.id)
#        qrimg = qrcode.make(self.qrtext)
#        qrimg.save("est/cv/img/qr/"+str(self.id)+".png", "PNG")
#        super(Trabajador, self).save(*args, **kwargs)
#
#

    def __unicode__(self):
        return u"%s %s %s" % (self.estid, self.nombre, self.centronegocios)

    def get_est_url(self):
        self.qrtext = "http://www.estchile.cl/cv/"+str(self.estid)
        return self.qrtext

    def get_absolute_url(self):
#        return reverse('est.views.card', args=[str(self.id)])
        self.qrtext = "http://www.estchile.cl/cv/"+str(self.estid)
        return self.qrtext

    def generate_qrimg(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=6,
            border=0,
        )

        qr.add_data(self.get_est_url())
#        qr.add_data(self.get_absolute_url())

        qr.make(fit=True)

        img = qr.make_image()

        buffer = StringIO.StringIO()
        img.save(buffer)
        filename = 'trabajador-%s.png' % (self.id)
        filebuffer = InMemoryUploadedFile(
            buffer, None, filename, 'image/png', buffer.len, None)
        self.qrimg.save(filename, filebuffer)


class TrabajadorDevice(models.Model):
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    device = models.ForeignKey(Devices, on_delete=models.CASCADE)
    fono_gps = models.IntegerField(blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __unicode__(self):
        return u"%s %s %s %s" % (self.trabajador, self.device, self.fecha_inicio, self.fecha_fin)


class TrabajadorEstudios(models.Model):
    trabajador = models.ForeignKey(Trabajador, blank=True, null=True, on_delete=models.CASCADE)
    estudio = models.ForeignKey(Estudios, blank=True, null=True, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    observacion = models.CharField(max_length=4096, blank=True, null=True)
    certificado = models.ImageField(upload_to='estudios/', blank=True, null=True)

    def __unicode__(self):
        return u"%s %s %s %s" % (self.trabajador, self.estudio, self.fecha_inicio, self.fecha_fin)


class TrabajadorCapacitacion(models.Model):
    trabajador = models.ForeignKey(Trabajador, blank=True, null=True, on_delete=models.CASCADE,)
    capacitacion = models.ForeignKey(Capacitacion, blank=True, null=True, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    observacion = models.CharField(max_length=4096, blank=True, null=True)
    certificado = models.ImageField(upload_to='capacitacion/', blank=True, null=True)

    def __unicode__(self):
        return u"%s %s %s %s" % (self.trabajador, self.capacitacion, self.fecha_inicio, self.fecha_fin)


