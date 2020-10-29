from django.shortcuts import render

from est.models import Planta, Zona, Trabajador, CentroNegocios

import qrcode

def curriculum(request, trabajador):

    trabajador = Trabajador.objects.get(estid=trabajador)

    context = {'trabajador': trabajador}

    return render(request,'cv/cv.html', context)

def machine(request, trabajador):

    trabajador = Trabajador.objects.get(estid=trabajador)

    context = {'trabajador': trabajador}

    return render(request,'cv/machine.html', context)

#    return render(request, '../templates/curriculum/classic.html', {
#        'resume': resume,
#        'skills': resume.skills.order_by('category', '-weight'),
#        'projects': resume.projects.order_by('-weight'),
#        'experiences': resume.experiences.order_by('-start_year'),
#        'trainings': resume.trainings.order_by('-year', '-month'),
#        'certifications': resume.certifications.order_by('-start_year', '-start_month')
#    })
#
#

def card(request, trabajador):

    trabajador = Trabajador.objects.get(estid=trabajador)
    trabajador.generate_qrimg()

    context = {'trabajador': trabajador,
#        'qrtext': qrtext,
#        'qrimg': qrimg,
    }

    return render(request,'cv/card.html', context)
