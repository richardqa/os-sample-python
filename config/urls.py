from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^', include('rest_framework_docs.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('phr.catalogo.api.urls', namespace='api-catalogo')),
    url(r'^api/', include('phr.ciudadano.api.urls', namespace='api-ciudadano')),
    url(r'^api/', include('phr.establecimiento.api.urls', namespace='api-establecimiento')),
    url(r'^api/', include('phr.insteducativa.api.urls', namespace='api-insteducativa')),
    url(r'^api/', include('phr.personal.api.urls', namespace='api-personal')),
    url(r'^api/', include('phr.ubigeo.api.urls', namespace='api-ubigeo')),
    url(r'^api/', include('phr.common.api.urls', namespace='api-common')),
    url(r'^api/v1/', include('rest_framework_docs.urls')),
    url(r'^api/v1/docs/', include('rest_framework_docs.urls')),
    url(r'reniec/', include('phr.reniec.urls', namespace='reniec')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
