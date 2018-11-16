# coding=utf-8
import json
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test.client import Client
from django.test.testcases import TestCase
from django.urls.base import reverse
from django.utils import timezone

from oauth2_provider.models import AccessToken, get_application_model
from oauth2_provider.settings import oauth2_settings
from phr.catalogo.models import CatalogoCIE
from phr.ciudadano.models import Ciudadano
from phr.ubigeo.models import UbigeoPais

Application = get_application_model()
UserModel = get_user_model()


class TestCiudadanoAPI(TestCase):
    fixtures = ['servicio.json']

    def setUp(self):
        self.client = Client()
        self.maxDiff = None
        oauth2_settings._SCOPES = ['read', 'write', 'scope1', 'scope2']

        self.test_user = UserModel.objects.create_user("test_user", "test@user.com", "123456")
        self.dev_user = UserModel.objects.create_user("dev_user", "dev@user.com", "123456")

        self.application = Application.objects.create(
            name="Test Application",
            redirect_uris="http://phr.minsa.local",
            user=self.dev_user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
        )

        self.access_token = AccessToken.objects.create(
            user=self.test_user,
            scope='read write',
            expires=timezone.now() + timedelta(seconds=300),
            token='secret-access-token-key',
            application=self.application
        )

    @staticmethod
    def _create_authorization_header(token):
        return "Bearer {0}".format(token)

    def test_ciudadano_ver(self):
        auth = self._create_authorization_header(self.access_token.token)
        url = reverse('api-ciudadano:v1:ciudadano:ver', kwargs={'numero_documento': 40404040})
        response = self.client.get(url, HTTP_AUTHORIZATION=auth)
        self.assertContains(response, '"numero_documento":"40404040"')

    def test_ciudadano_crear_sindocumento(self):
        auth = self._create_authorization_header(self.access_token.token)
        url = reverse("api-ciudadano:v1:ciudadano:crear_data")
        payload = {
            "nombres": "DAVIS ABEL",
            "apellido_paterno": "BENITO",
            "apellido_materno": "LLANA",
            "sexo": "1",
            "fecha_nacimiento": "1984-08-18",
            "tipo_documento": '00',
            "numero_documento": ''
        }
        response = self.client.post(url, payload, HTTP_AUTHORIZATION=auth)
        self.assertContains(response, '"numero_documento":"SD-00000001"', status_code=201)


class TestAntecedentePersonal(TestCase):
    def setUp(self):
        self.client = Client()
        CatalogoCIE.objects.create(id=1, id_ciex='M610', desc_ciex='Algo malo')
        UbigeoPais.objects.create(id=177)
        Ciudadano.objects.create(id=1, tipo_documento_minsa='1', numero_documento='44332211', nombres='Pepito')

    def test_registrar_antecedente_personal(self):
        url = reverse("api-ciudadano:v1:ciudadano:antecedente-crear")
        payload = {
            'tipo_documento': '1',
            'numero_documento': '44332211',
            'id_ciex': 'M610',
            'fecha_inicio': '2017-04-15',
            'fecha_fin': '2017-04-26',
            'observaciones': '',
            'tipo_antecedente': '1',
        }
        response = self.client.post(url, payload)
        result = {"fecha_inicio": "2017-04-15", "observaciones": "", "ciex": {"id": "1", "type": "CatalogoCIE"},
                  "ciudadano": {"id": "1", "type": "Ciudadano"}, "fecha_fin": "2017-04-26", "es_removido": False,
                  "tipo_antecedente": "1"}
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(json.dumps(response.json()), json.dumps(result))

    def test_registrar_antecedente_familiar(self):
        """Antecedente familiar"""
        url = reverse("api-ciudadano:v1:ciudadano:antecedentefam-crear")
        payload = {
            'tipo_documento': '1',
            'numero_documento': '44332211',
            'id_ciex': 'M610',
            'parentesco': 2,
            'fecha_inicio': '2017-04-15',
            'fecha_fin': '2017-04-26',
            'observaciones': '',
        }
        response = self.client.post(url, payload)
        result = {"fecha_inicio": "2017-04-15", "observaciones": "", "ciex": {"id": "1", "type": "CatalogoCIE"},
                  "ciudadano": {"id": "1", "type": "Ciudadano"}, "fecha_fin": "2017-04-26", "es_removido": False,
                  "parentesco": 2}
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(json.dumps(response.json()), json.dumps(result))
