import json

from django.test.client import Client
from django.test.testcases import TestCase

from phr.ubigeo.models import UbigeoPais


class TestReniec(TestCase):
    def setUp(self):
        self.client = Client()
        UbigeoPais.objects.create(id=177)

    def test_registro_reniec(self):
        url = "/reniec/cnv/"
        payload = {
            "NUMERO_CNV": "1000167506",
            "TIPO_DOC_MADRE": "01",
            "NUMERO_DOC_MADRE": "10101010___________________________",
            "PRIMER_APELLIDO_MADRE": "QUIJO___________________________________",
            "SEGUNDO_APELLIDO_MADRE": "COAQUIRA________________________________",
            "PRENOMBRES_MADRE": "EDITH_______________________________________________________",
            "SEXO_NACIDO": "02",
            "FECHA_NACIDO": "20130626",
            "HORA_NACIDO": "134500",
            "PESO_NACIDO": "3340",
            "TALLA_NACIDO": "50__",
            "APGAR_UNO_NACIDO": "9_",
            "APGAR_CINCO_NACIDO": "9_",
            "ETNIA_NACIDO": "__",
            "NU_NACIDO_PERIM_CEFALICO": "45.2",
            "NU_NACIDO_PERIM_TORACICO": "49.9",
            "NU_TEMPERATURA": "37",
            "CO_RESULTADO_EF": "01",
            "NU_EDAD_EXAMEN_FISICO": "12",
            "CO_UM_EDAD": "02",
            "DURACION_EMBARAZO_PARTO": "41",
            "ATIENDE_PARTO": "02",
            "CONDICION_PARTO": "01",
            "TIPO_PARTO": "01",
            "FINANCIADOR_PARTO": "01",
            "CO_POSICION_PARTO": "01",
            "IN_PARTOGRAMA": 1,
            "IN_ACOMPANA_PARTO": 1,
            "CO_DURACION_PARTO": "01",
            "IN_EPISIOTOMIA_PARTO": "01",
            "IN_DESGARRO_PARTO": "01",
            "CO_ALUMBRAMIENTO_PARTO": "01",
            "IN_PLACENTA_PARTO": "01",
            "IN_EESS_PROCEDENCIA": "01",
            "CO_EESS_PROCENDENCIA": "00006208",
            "CODIGO_LOCAL": "00006208",
            "CODIGO_RENAES": "00006208",
            "CODIGO_OPERACION": "01"
        }
        response = self.client.post(url, payload)
        result = {"CODIGO_OPERACION": "01", "NUMERO_CNV": "1000167506"}
        self.assertJSONEqual(json.dumps(response.json()), json.dumps(result))

    def test_registro_edicion_reniec(self):
        url_registro = "/reniec/cnv/"
        url_edicion = "/reniec/cnv/"
        payload_registro = {
            "NUMERO_CNV": "1000167506",
            "TIPO_DOC_MADRE": "01",
            "NUMERO_DOC_MADRE": "10101010___________________________",
            "PRIMER_APELLIDO_MADRE": "QUIJO___________________________________",
            "SEGUNDO_APELLIDO_MADRE": "COAQUIRA________________________________",
            "PRENOMBRES_MADRE": "EDITH_______________________________________________________",
            "SEXO_NACIDO": "02",
            "FECHA_NACIDO": "20130626",
            "HORA_NACIDO": "134500",
            "PESO_NACIDO": "3340",
            "TALLA_NACIDO": "50__",
            "APGAR_UNO_NACIDO": "9_",
            "APGAR_CINCO_NACIDO": "9_",
            "ETNIA_NACIDO": "__",
            "NU_NACIDO_PERIM_CEFALICO": "45.2",
            "NU_NACIDO_PERIM_TORACICO": "49.9",
            "NU_TEMPERATURA": "37",
            "CO_RESULTADO_EF": "01",
            "NU_EDAD_EXAMEN_FISICO": "12",
            "CO_UM_EDAD": "02",
            "DURACION_EMBARAZO_PARTO": "41",
            "ATIENDE_PARTO": "02",
            "CONDICION_PARTO": "01",
            "TIPO_PARTO": "01",
            "FINANCIADOR_PARTO": "01",
            "CO_POSICION_PARTO": "01",
            "IN_PARTOGRAMA": 1,
            "IN_ACOMPANA_PARTO": 1,
            "CO_DURACION_PARTO": "01",
            "IN_EPISIOTOMIA_PARTO": "01",
            "IN_DESGARRO_PARTO": "01",
            "CO_ALUMBRAMIENTO_PARTO": "01",
            "IN_PLACENTA_PARTO": "01",
            "IN_EESS_PROCEDENCIA": "01",
            "CO_EESS_PROCENDENCIA": "00006208",
            "CODIGO_LOCAL": "00006208",
            "CODIGO_RENAES": "00006208",
            "CODIGO_OPERACION": "01"
        }
        response_registro = self.client.post(url_registro, payload_registro)
        result = {"CODIGO_OPERACION": "01", "NUMERO_CNV": "1000167506"}
        self.assertJSONEqual(json.dumps(response_registro.json()), json.dumps(result))

        payload_edicion = payload_registro.copy()
        payload_edicion.update(
            {"NUMERO_CNV": "1000167507", "NU_NACIDO_PERIM_CEFALICO": "42.5", "NU_NACIDO_PERIM_TORACICO": "47.8",
             "CODIGO_OPERACION": "02"})
        response_edicion = self.client.post(url_edicion, payload_edicion)
        result = {"CODIGO_OPERACION": "02", "NUMERO_CNV": "1000167507"}
        self.assertJSONEqual(json.dumps(response_edicion.json()), json.dumps(result))
