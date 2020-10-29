from django.contrib.gis.db import models
from est.models import Zona, Contacto

class Tiempozona(models.Model):

    def __init__(self,id, nombre, dias, horas, minutos, primero, ultimo, dif):
	self.id=id
	self.nombre = nombre
	self.dias = dias
	self.horas = horas
	self.minutos = minutos
        self.primero = primero
        self.ultimo = ultimo
        self.dif = dif

class Rangozona(object):

    def __init__(self, zona, inicio, fin):

        self.zona = zona
        self.inicio = inicio
        self.fin = fin 

class Listatrabajadores(models.Model):
    
    def __init__( self):
        self.nombre = None
	self.id = None
	self.lat=None
	self.lon=None
	self.apellidop=None
	self.apellidom=None
	self.fono=None
	self.cargo=None
	self.i=None

class Listaplantas(models.Model):

    def __init__(self, id, nombre,lat,lon):
	self.id = id
	self.nombre=nombre
	self.lat=lat
	self.lon=lon

class Listacn(models.Model):

    def __init__(self):
	self.nombre= None
	self.id= None	

class Posicionestrabajador(models.Model):
	#    protocol = models.CharField(max_length=128, blank=True, null=True)
	deviceid = models.IntegerField(blank=True, null=True)
	#    servertime = models.DateTimeField(db_column='serverTime')  # Field name made lowercase.
	#    devicetime = models.DateTimeField(db_column='deviceTime')  # Field name made lowercase.
	fixtime = models.DateTimeField(db_column='fixTime')  # Field name made lowercase.
	valid = models.BooleanField()
	lat = models.FloatField()
	lon = models.FloatField()
	#    altitude = models.FloatField()
	#    speed = models.FloatField()
	#    course = models.FloatField()
	address = models.CharField(max_length=512, blank=True, null=True)
	attributes = models.CharField(max_length=4096)
	geom = models.PointField(db_column='punto', srid=4326)#, default='SRID=4326;POINT(9.0 9.0)')
	#    objects = models.GeoManager()
	TIPO_CONTACTO_CHOICES = (
	('PADRE','Padre'),
	('MADRE','Madre'),
	('ESPOSO','Esposa(o)'),
	('ABUELO','Abuelo(a)'),
	('HIJO','Hijo(a)'),
	('PAREJA','Pareja'),
	('POLOLO','Pololo(a)')
	)

	nombre = models.CharField(max_length=128, blank=True, null=True)
	apellidop = models.CharField(max_length=128, blank=True, null=True)
	apellidom = models.CharField(max_length=128, blank=True, null=True)
	#foto = models.ImageField(upload_to='est/static/cv/img/', blank=True, null=True)
	fecha_nac = models.DateField(blank=True, null=True)
	direccion = models.CharField(max_length=256, blank=True, null=True)
	
	fono = models.IntegerField(blank=True, null=True)
	e_mail = models.CharField(max_length=128, blank=True, null=True)
	emergencia =models.IntegerField(blank=True, null=True)
	tipo_contacto = models.CharField(max_length=128, blank=True, null=True, choices=TIPO_CONTACTO_CHOICES)
	rut = models.CharField(max_length=128, blank=True, null=True)
	centroNegocios = models.IntegerField(blank=True, null=True)
	cargo = models.CharField(max_length=128, blank=True, null=True)
	rol = models.IntegerField(blank=True, null=True)
	gps = models.IntegerField(blank=True, null=True)
	supervisor = models.IntegerField(blank=True, null=True)
	empresa = models.IntegerField(blank=True, null=True)
	salud = models.IntegerField(blank=True, null=True)
	estudios = models.IntegerField(blank=True, null=True)     
	capacitacion = models.IntegerField(blank=True, null=True)
	nivel_riesgo = models.IntegerField(blank=True, null=True)
	nota = models.CharField(max_length=256, blank=True, null=True)
	nota2 = models.CharField(max_length=256, blank=True, null=True)

class Alertatrabajador(models.Model):
	#    protocol = models.CharField(max_length=128, blank=True, null=True)
	#deviceid = models.IntegerField(blank=True, null=True)
	#    servertime = models.DateTimeField(db_column='serverTime')  # Field name made lowercase.
	#    devicetime = models.DateTimeField(db_column='deviceTime')  # Field name made lowercase.
	#fixtime = models.DateTimeField(db_column='fixTime')  # Field name made lowercase.
	#valid = models.BooleanField()
	#lat = models.FloatField()
	#lon = models.FloatField()
	#    altitude = models.FloatField()
	#    speed = models.FloatField()
	#    course = models.FloatField()
	#address = models.CharField(max_length=512, blank=True, null=True)
	#attributes = models.CharField(max_length=4096)
	geom = models.PointField(db_column='punto', srid=4326)#, default='SRID=4326;POINT(9.0 9.0)')
	#    objects = models.GeoManager()
	TIPO_CONTACTO_CHOICES = (
	('PADRE','Padre'),
	('MADRE','Madre'),
	('ESPOSO','Esposa(o)'),
	('ABUELO','Abuelo(a)'),
	('HIJO','Hijo(a)'),
	('PAREJA','Pareja'),
	('POLOLO','Pololo(a)')
	)
	i=models.IntegerField(blank=True, null=True)
	zona=models.CharField(max_length=128, blank=True, null=True)
	nombre = models.CharField(max_length=128, blank=True, null=True)
	#apellidop = models.CharField(max_length=128, blank=True, null=True)
	#apellidom = models.CharField(max_length=128, blank=True, null=True)
	#foto = models.ImageField(upload_to='est/static/cv/img/', blank=True, null=True)
	#fecha_nac = models.DateField(blank=True, null=True)
	#direccion = models.CharField(max_length=256, blank=True, null=True)
	foto=models.CharField(max_length=128, blank=True, null=True)
	fono = models.IntegerField(blank=True, null=True)
	#e_mail = models.CharField(max_length=128, blank=True, null=True)
	nombre_emergencia =models.CharField(max_length=128, blank=True, null=True)
	nro_emergencia =models.CharField(max_length=128, blank=True, null=True)
	tipo_contacto = models.CharField(max_length=128, blank=True, null=True, choices=TIPO_CONTACTO_CHOICES)
	#rut = models.CharField(max_length=128, blank=True, null=True)
	#centroNegocios = models.IntegerField(blank=True, null=True)
	cargo = models.CharField(max_length=128, blank=True, null=True)
	#rol = models.IntegerField(blank=True, null=True)
	#gps = models.IntegerField(blank=True, null=True)
	#supervisor = models.IntegerField(blank=True, null=True)
	#empresa = models.IntegerField(blank=True, null=True)
	#salud = models.IntegerField(blank=True, null=True)
	#estudios = models.IntegerField(blank=True, null=True)     
	#capacitacion = models.IntegerField(blank=True, null=True)
	nivel_riesgo = models.IntegerField(blank=True, null=True)
	#nota = models.CharField(max_length=256, blank=True, null=True)
	#nota2 = models.CharField(max_length=256, blank=True, null=True)

class testzona(models.Model):
	
	zona=models.CharField(max_length=128, blank=True, null=True)
	nombre = models.CharField(max_length=128, blank=True, null=True)
	#apellidop = models.CharField(max_length=128, blank=True, null=True)
	#apellidom = models.CharField(max_length=128, blank=True, null=True)
	#foto = models.ImageField(upload_to='est/static/cv/img/', blank=True, null=True)
	#fecha_nac = models.DateField(blank=True, null=True)
	#direccion = models.CharField(max_length=256, blank=True, null=True)
	#foto=models.CharField(max_length=128, blank=True, null=True)
	#fono = models.IntegerField(blank=True, null=True)
	#e_mail = models.CharField(max_length=128, blank=True, null=True)
	#nombre_emergencia =models.CharField(max_length=128, blank=True, null=True)
	#nro_emergencia =models.CharField(max_length=128, blank=True, null=True)
	#tipo_contacto = models.CharField(max_length=128, blank=True, null=True, choices=TIPO_CONTACTO_CHOICES)
	#rut = models.CharField(max_length=128, blank=True, null=True)
	#centroNegocios = models.IntegerField(blank=True, null=True)
	#cargo = models.CharField(max_length=128, blank=True, null=True)
	#rol = models.IntegerField(blank=True, null=True)
	#gps = models.IntegerField(blank=True, null=True)
	#supervisor = models.IntegerField(blank=True, null=True)
	#empresa = models.IntegerField(blank=True, null=True)
	#salud = models.IntegerField(blank=True, null=True)
	#estudios = models.IntegerField(blank=True, null=True)     
	#capacitacion = models.IntegerField(blank=True, null=True)
	#nivel_riesgo = models.IntegerField(blank=True, null=True)
	#nota = models.CharField(max_length=256, blank=True, null=True)
	#nota2 = models.CharField(max_length=256, blank=True, null=True)
