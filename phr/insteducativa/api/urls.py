from django.conf.urls import include, url

from phr.insteducativa.api.views import (
    InstEducativaCrearAPIView, InstEducativaDataAPIView, InstEducativaListAPIView, InstEducativaUbigeoAPIView,
)

urlpatterns = [
    url(r'^v1/', include([
        url(r'^insteducativa/', include([
            url(r'^lista/$', InstEducativaListAPIView.as_view(), name='lista'),
            url(r'^ubigeo/(?P<ubigeo>\d{2,6})/$', InstEducativaUbigeoAPIView.as_view(), name='ubigeo'),
            url(r'^detalle/(?P<codigo_modular>\d+)/$', InstEducativaDataAPIView.as_view(), name='data'),
            url(r'^crear/$', InstEducativaCrearAPIView.as_view(), name='crear'),
        ], namespace='insteducativa')),
    ], namespace='v1')),
]
