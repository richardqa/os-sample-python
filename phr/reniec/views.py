# coding=utf-8
from datetime import datetime

from rest_framework.generics import CreateAPIView, DestroyAPIView, RetrieveUpdateAPIView
from rest_framework.parsers import JSONParser
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

from phr.ciudadano.models import CiudadanoRN
from phr.common.constants import INACTIVO
from phr.reniec.serializers import CiudadanoRNSerializer


def obtener_datos_ciudadanorn(payload):
    """
    Obtiene datos de CiudadanoRN utilizando la trama enviada por RENIEC

    :param payload: Trama enviada por RENIEC
    :return: Trama de datos de Ciudadano RN
    """
    numero_cnv = payload.get("numero_cnv", "").replace("_", "")
    tipo_doc_madre = payload.get("tipo_doc_madre", "").replace("_", "")
    numero_doc_madre = payload.get("numero_doc_madre", "").replace("_", "")
    primer_apellido_madre = payload.get("primer_apellido_madre", "").replace("_", "")
    segundo_apellido_madre = payload.get("segundo_apellido_madre", "").replace("_", "")
    prenombres_madre = payload.get("prenombres_madre", "").replace("_", "")
    sexo_nacido = payload.get("sexo_nacido", "").replace("_", "")[1:]
    fecha_nacido = payload.get("fecha_nacido", "").replace("_", "")
    if fecha_nacido:
        fecha_nacido = datetime.strptime(fecha_nacido, "%Y%m%d").date()
    hora_nacido = payload.get("hora_nacido", "").replace("_", "")
    if hora_nacido:
        hora_nacido = datetime.strptime(hora_nacido, "%H%M%S").time()
    peso_nacido = payload.get("peso_nacido", "0").replace("_", "")
    talla_nacido = payload.get("talla_nacido", "0").replace("_", "")
    apgar_uno_nacido = payload.get("apgar_uno_nacido", "0").replace("_", "")
    apgar_cinco_nacido = payload.get("apgar_cinco_nacido", "0").replace("_", "")
    etnia_nacido = payload.get("etnia_nacido", "80").replace("_", "")
    nu_nacido_perim_cefalico = payload.get("nu_nacido_perim_cefalico", "0").replace("_", "")
    nu_nacido_perim_toracico = payload.get("nu_nacido_perim_toracico", "0").replace("_", "")
    duracion_embrazado_parto = payload.get("duracion_embarazo_parto", "").replace("_", "")
    atiende_parto = payload.get("atiende_parto", "").replace("_", "")
    condicion_parto = payload.get("condicion_parto", "").replace("_", "")
    tipo_parto = payload.get("tipo_parto", "").replace("_", "")
    financiador_parto = str(int(payload.get("financiador_parto", "0").replace("_", "")))
    codigo_local = payload.get("codigo_local", "").replace("_", "")
    codigo_renaes = payload.get("codigo_renaes", "").replace("_", "")
    codigo_renaes_adscrito = payload.get("codigo_renaes_adscrito", "").replace("_", "")

    ciudadano_rn_data = {
        "cui": numero_cnv,
        "tipo_doc_madre": tipo_doc_madre,
        "numero_doc_madre": numero_doc_madre,
        "primer_apellido_madre": primer_apellido_madre,
        "segundo_apellido_madre": segundo_apellido_madre,
        "prenombres_madre": prenombres_madre,
        "sexo_nacido": sexo_nacido,
        "fecha_nacimiento": fecha_nacido,
        "hora_nacimiento": hora_nacido,
        "peso_nacido": peso_nacido,
        "talla_nacido": talla_nacido,
        "apgar_uno_nacido": apgar_uno_nacido,
        "apgar_cinco_nacido": apgar_cinco_nacido,
        "etnia": etnia_nacido,
        "numero_nacido_perim_cefalico": nu_nacido_perim_cefalico,
        "numero_nacido_perim_toracico": nu_nacido_perim_toracico,
        "duracion_semanas_parto": duracion_embrazado_parto,
        "atiende_parto": atiende_parto,
        "condicion_parto": condicion_parto,
        "tipo_parto": tipo_parto,
        "financiador_parto": financiador_parto,
        "codigo_local": codigo_local,
        "codigo_renaes": codigo_renaes,
        "codigo_renaes_adscrito": codigo_renaes_adscrito,
    }
    return ciudadano_rn_data


class CrearCiudadanoRN(CreateAPIView):
    """
    Registra  datos de ciudadano recibidos desde RENIEC
    """
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)
    serializer_class = CiudadanoRNSerializer

    def create(self, request, *args, **kwargs):
        ciudadano_rn_data = obtener_datos_ciudadanorn(request.data)
        cod_operacion = request.data.get('codigo_operacion', '')
        if cod_operacion and cod_operacion == "02":
            try:
                instance = CiudadanoRN.objects.get(
                    es_ficha_activa=True, es_removido=False, cui=request.data.get('numero_cnv', ''))
                serializer = self.get_serializer(instance, data=ciudadano_rn_data, partial=False)
            except:
                return Response(status=HTTP_404_NOT_FOUND)
        else:
            serializer = self.get_serializer(data=ciudadano_rn_data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)


class VerActualizarEliminarCiudadanoRN(RetrieveUpdateAPIView, DestroyAPIView):
    """
    Obtiene, actualiza o elimina datos de ciudadano RN con trama enviada desde RENIEC
    """
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)
    serializer_class = CiudadanoRNSerializer
    lookup_field = 'cui'
    queryset = CiudadanoRN.objects.filter(es_ficha_activa=True, es_removido=False)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.es_ficha_activa = False
        instance.es_removido = True
        instance.ciudadano.es_removido = True
        instance.ciudadano.estado = INACTIVO
        instance.save()
        return Response(status=HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=obtener_datos_ciudadanorn(request.data), partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
