from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^v1/', include([
        url(r'^ciudadano-autocomplete$', views.CiudadanoAutocomplete.as_view(), name='ciudadano_autocomplete'),
        url(r'^establecimiento/(?P<renaes>\d+)/personal/$', views.PersonalEstablecimiento.as_view(),
            name='personal_establecimiento'),
        url(r'^personal/(?P<cmp>\d+)/$', views.PersonalView.as_view(), name='personal_ver'),
        url(r'^personal/(?P<cmp>\d+)/(?P<dni>\d{8})/$', views.PersonalCiudadanoView.as_view(),
            name='personal_ciudadano_ver'),
        url(r'^personal/ciudadano/(?P<dni>\d+)/$', views.CiudadanoPersonalView.as_view()),
    ], namespace='v1')),

]
