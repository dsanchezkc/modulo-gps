# Auto-generated `LayerMapping` dictionary for Zona model

import os
from django.contrib.gis.utils import LayerMapping
from .models import Zona

zona_mapping = {
#    'id' : 'id',
    'nombre' : 'nombre',
#    'amenaza' : 'amenaza',
#    'nivel' : 'nivel',
    'uso' : 'uso',
    'zona' : 'POLYGON',
}

edificacion_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', 'Edificacion/Edificacion.shp'))

def run(verbose=True):
    lm = LayerMapping(Zona, edificacion_shp, zona_mapping,
                      transform=False, encoding='latin-1')

    lm.save(strict=True, verbose=verbose)

