from django.conf.urls import url

from phr.common.api.views import ConnectionStatusAPI

urlpatterns = [
    url(r'connection-status/$', ConnectionStatusAPI.as_view()),
]
