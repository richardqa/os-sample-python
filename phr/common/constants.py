"""
Constantes para el proyecto
"""

ACTIVO = '1'

INACTIVO = '2'

PENDIENTE = '3'

STATUS_MODEL = (
    (ACTIVO, 'Activo'),
    (INACTIVO, 'Inactivo'),
    (PENDIENTE, 'Pendiente'),
)


ORIGEN_DATA_IMPORTADO = 1

ORIGEN_DATA_HISMINSA = 2

ORIGEN_DATA_RENIEC = 3

ORIGEN_DATA_CNV = 4

ORIGEN_DATA_CREADO = 5

ORIGEN_DATA_MIGRACIONES = 6

ORIGEN_DATA_CHOICES = (
    (ORIGEN_DATA_IMPORTADO, 'importado'),
    (ORIGEN_DATA_HISMINSA, 'hisminsa'),
    (ORIGEN_DATA_RENIEC, 'búsqueda reniec'),
    (ORIGEN_DATA_CNV, 'cnv'),
    (ORIGEN_DATA_CREADO, 'creado'),
    (ORIGEN_DATA_MIGRACIONES, 'búsqueda migraciones'),
)


RENIEC_CODIGO_DATA_CORRECTO = '0000'

ETNIA_MESTIZO = '58'

ETNIA_CHOICES = (
    ('01', 'Achuar'),
    ('02', 'Aimara'),
    ('03', 'Amahuaca'),
    ('04', 'Arabela'),
    ('05', 'Ashaninka'),
    ('06', 'Asheninka'),
    ('07', 'Awajún'),
    ('08', 'Bora'),
    ('09', 'Capanahua'),
    ('10', 'Cashinahua'),
    ('11', 'Chamicuro'),
    ('12', 'Chapra'),
    ('13', 'Chitonahua'),
    ('14', 'Ese eja'),
    ('15', 'Harakbut'),
    ('16', 'Ikitu'),
    ('17', 'Iñapari'),
    ('18', 'Isconahua'),
    ('19', 'Jaqaru'),
    ('20', 'Jíbaro'),
    ('21', 'Kakataibo'),
    ('22', 'Kakinte'),
    ('23', 'Kandozi'),
    ('24', 'Kichwa'),
    ('25', 'Kukama kukamiria'),
    ('26', 'Madija'),
    ('27', 'Maijuna'),
    ('28', 'Marinahua'),
    ('29', 'Mashco Piro'),
    ('30', 'Mastanahua'),
    ('31', 'Matsés'),
    ('32', 'Matsigenka'),
    ('33', 'Muniche'),
    ('34', 'Murui-muinanɨ'),
    ('35', 'Nahua'),
    ('36', 'Nanti'),
    ('37', 'Nomatsigenga'),
    ('38', 'Ocaina'),
    ('39', 'Omagua'),
    ('40', 'Quechuas'),
    ('41', 'Resígaro'),
    ('42', 'Secoya'),
    ('43', 'Sharanahua'),
    ('44', 'Shawi'),
    ('45', 'Shipibo-konibo'),
    ('46', 'Shiwilu'),
    ('47', 'Tikuna'),
    ('48', 'Urarina'),
    ('49', 'Uro'),
    ('50', 'Vacacocha'),
    ('51', 'Wampis'),
    ('52', 'Yagua'),
    ('53', 'Yaminahua'),
    ('54', 'Yanesha'),
    ('55', 'Yine'),
    ('56', 'Afrodescendiente'),
    ('57', 'Blanco'),
    (ETNIA_MESTIZO, 'Mestizo'),
    ('59', 'Otro'),
    ('60', 'No sabe / No responde')
)


LENGUA_CASTELLANO = 'CASTELLANO'

LENGUA_QUECHUA = 'QUECHUA'

LENGUA_AYMARA = 'AYMARA'

LENGUA_AMAZONICA = 'AMAZONICA'

LENGUA_OTRO = 'OTRO'

LENGUA_CHOICES = (
    (LENGUA_CASTELLANO, 'Castellano'),
    (LENGUA_QUECHUA, 'Quechua'),
    (LENGUA_AYMARA, 'Aymara'),
    (LENGUA_AMAZONICA, 'Nativo amazónico'),
    (LENGUA_OTRO, 'Otro'),
)


ESTADO_CIVIL_SOLTERO = '1'

ESTADO_CIVIL_CASADO = '2'

ESTADO_CIVIL_CONVIVIENTE = '3'

ESTADO_CIVIL_DIVORCIADO = '4'

ESTADO_CIVIL_VIUDO = '5'

ESTADO_CIVIL_SEPARADO = '6'

ESTADO_CIVIL_CHOICES = (
    (ESTADO_CIVIL_SOLTERO, 'Soltero(a)'),
    (ESTADO_CIVIL_CASADO, 'Casado(a)'),
    (ESTADO_CIVIL_CONVIVIENTE, 'Conviviente'),
    (ESTADO_CIVIL_DIVORCIADO, 'Divorciado(a)'),
    (ESTADO_CIVIL_VIUDO, 'Viudo(a)'),
    (ESTADO_CIVIL_SEPARADO, 'Separado(a)'),
)


SEXO_MASCULINO = '1'

SEXO_FEMENINO = '2'

SEXO_CHOICES = (
    (SEXO_MASCULINO, 'Masculino'),
    (SEXO_FEMENINO, 'Femenino'),
)


TIPODOC_NO_SE_CONOCE = '00'

TIPODOC_DNI = '01'

TIPODOC_LIBRETA_MILITAR = '02'

TIPODOC_CARNET_EXTRANJERIA = '03'

TIPODOC_ACTA_NACIMIENTO = '04'

TIPODOC_PASAPORTE = '06'

TIPODOC_DNI_EXTRANJERO = '07'

TDOC_CHOICES = (
    (TIPODOC_NO_SE_CONOCE, 'NO SE CONOCE'),
    (TIPODOC_DNI, 'DNI/LE'),
    (TIPODOC_LIBRETA_MILITAR, 'LM/BO'),
    (TIPODOC_CARNET_EXTRANJERIA, 'CARNET DE EXTRAJERIA'),
    (TIPODOC_ACTA_NACIMIENTO, 'ACTA DE NACIMIENTO'),
    (TIPODOC_PASAPORTE, 'PASAPORTE'),
    (TIPODOC_DNI_EXTRANJERO, 'DI DEL EXTRANJERO'),
)

TIPODOC_CARNET_EXTRANJERIA_MIGRACIONES = 'CE'

TDOC_HISMINSA_NO_TIENE = '0'

TDOC_HISMINSA_DNI = '1'

TDOC_HISMINSA_CARNET_EXTRANJERIA = '2'

TDOC_HISMINSA_PASAPORTE = '3'

TDOC_HISMINSA_DNI_EXTRANJERO = '4'

TDOC_CHOICES_HISMINSA = (
    (TDOC_HISMINSA_NO_TIENE, 'No tiene'),
    (TDOC_HISMINSA_DNI, 'DNI'),
    (TDOC_HISMINSA_CARNET_EXTRANJERIA, 'Carné de extranjería'),
    (TDOC_HISMINSA_PASAPORTE, 'Pasaporte'),
    (TDOC_HISMINSA_DNI_EXTRANJERO, 'Documento de identidad extranjero'),
)


FINANCIADOR_NO_SE_CONOCE = '0'

FINANCIADOR_USUARIO = '1'

FINANCIADOR_SIS = '2'

FINANCIADOR_ESSALUD = '3'

FINANCIADOR_SOAT = '4'

FINANCIADOR_SANIDAD_FAP = '5'

FINANCIADOR_SANIDAD_NAVAL = '6'

FINANCIADOR_SANIDAD_EP = '7'

FINANCIADOR_SANIDAD_PNP = '8'

FINANCIADOR_PRIVADO = '9'

FINANCIADOR_OTROS = '10'

FINANCIADOR_EXONERADO = '11'

FINANCIADOR_CHOICES = (
    (FINANCIADOR_NO_SE_CONOCE, 'NO SE CONOCE'),
    (FINANCIADOR_USUARIO, 'USUARIO'),
    (FINANCIADOR_SIS, 'SIS'),
    (FINANCIADOR_ESSALUD, 'ESSALUD'),
    (FINANCIADOR_SOAT, 'S.O.A.T'),
    (FINANCIADOR_SANIDAD_FAP, 'SANIDAD F.A.P'),
    (FINANCIADOR_SANIDAD_NAVAL, 'SANIDAD NAVAL'),
    (FINANCIADOR_SANIDAD_EP, 'SANIDAD EP'),
    (FINANCIADOR_SANIDAD_PNP, 'SANIDAD PNP'),
    (FINANCIADOR_PRIVADO, 'PRIVADOS'),
    (FINANCIADOR_OTROS, 'OTROS'),
    (FINANCIADOR_EXONERADO, 'EXONERADO'),
)

SIS_ESTADO_ACTIVO = 'ACTIVO'

AP_CHOICES = (
    ('00', 'NO SE CONOCE'),
    ('01', 'MÉDICO'),
    ('02', 'OBSTETRA'),
    ('03', 'ENFERMERA (O)'),
    ('04', 'INTERNA (O)'),
    ('05', 'TÉCNICO SALUD'),
    ('06', 'PROMOTOR SALUD'),
    ('07', 'PARTERA / COMADRONA'),
    ('08', 'FAMILIAR'),
    ('09', 'OTRO'),
    ('10', 'NADIE (AUTOAYUDA)'),
    ('11', 'MÉDICO GINECO-OBSTETRA'),
    ('16', 'MÉDICO RESIDENTE'),
    ('99', 'NO REGISTRADO'),
)

PEG_CHOICES = (
    ('01', 'Adecuado'),
    ('02', 'Pequeño'),
    ('03', 'Grande'),
)

REARESP_CHOICES = (
    ('00', 'No'),
    ('01', 'Oxígeno'),
    ('02', 'Bolsa y máscara'),
    ('03', 'Avanzado'),
)

REF_CHOICES = (
    ('01', 'Normal'),
    ('02', 'Patologico'),
)

MUERTEINTRA_PARTO_CHOICES = (
    ('01', 'No hubo'),
    ('02', 'Durante embarazo'),
    ('03', 'Durante parto'),
    ('04', 'Momento desconocido')
)

EPISIOTOMIA_PARTO_CHOICES = (
    ('01', 'Sí'),
    ('02', 'No'),
    ('04', 'No aplica'),
)

POSICION_CHOICES = (
    ('01', 'Horizontal'),
    ('02', 'Vertical'),
    ('03', 'No aplica'),
)

DURACION_PARTO_CHOICES = (
    ('01', 'Normal'),
    ('02', 'Prolongado'),
    ('03', 'Precipitado'),
    ('04', 'No aplica'),
)

DESGARRO_PARTO_CHOICES = (
    ('00', 'No hubo'),
    ('01', 'I'),
    ('02', 'II'),
    ('03', 'III/IV'),
)

SIGNOS_SINTOMAS_ALERTAS_CHOICES = (
    ('01', 'Anasarca'),
    ('02', 'Cianosis'),
    ('03', 'Escotomas'),
    ('04', 'Hematuria'),
    ('05', 'Hipertensión ortostática'),
    ('06', 'Ictericia'),
    ('07', 'Petequias'),
    ('08', 'Proteinuria'),
    ('09', 'Dolor en hipocondrio derecho'),
)

CA_CHOICES = (
    ('01', 'No recibe'),
    ('02', 'Completo'),
    ('03', 'Incompleto'),
)

CTP_CHOICES = (
    ('00', 'No se conoce'),
    ('01', 'Espontáneo'),
    ('02', 'Instrumentado'),
    ('03', 'Cesárea'),
    ('04', 'Otro'),
)

TP_CHOICES = (
    ('01', 'Único'),
    ('02', 'Doble'),
    ('03', 'Triple'),
    ('04', 'Más de tres'),
)

PP_CHOICES = (
    ('01', 'Completa'),
    ('02', 'Incompleta'),
    ('03', 'Retenida'),
)

DEP_CHOICES = (
    ('01', 'Meconial'),
    ('02', 'Transaccional'),
    ('03', 'Amarilla'),
)

ALIM_CHOICES = (
    ('01', 'Lactancia materna exclusiva'),
    ('02', 'Mixta'),
    ('03', 'Artificial'),
)

GRUPOSANG_CHOICES = (
    ('01', 'O'),
    ('02', 'A'),
    ('03', 'B'),
    ('04', 'AB'),
)

SIGNOS_NULL_CHOICES = (
    ('01', '+'),
    ('02', '-'),
    ('03', 'No se hizo'),
)

TIPOE_CHOICES = (
    ('01', 'Sano'),
    ('02', 'Translado'),
    ('03', 'Con patología'),
    ('04', 'Fallecido'),
)

UM_EDAD_CHOICES = (
    ('01', 'Horas'),
    ('02', 'Días'),
)

INMUNIZACION_CHOICES = (
    ('1', 'BCG'),
    ('2', 'HVB')
)

FICHA_RN_STATUS_CHOICES = (
    ('01', 'Activa'),
    ('02', 'Inactiva'),
)

GI_CHOICES = (
    ('00', 'Sin instrucción'),
    ('01', 'Educación inicial'),
    ('02', 'Primaria completa'),
    ('03', 'Primaria incompleta'),
    ('04', 'Educación especial'),
    ('05', 'Secundaria completa'),
    ('06', 'Secundaria cncompleta'),
    ('07', 'Superior técnica completa'),
    ('08', 'Superior técnica incompleta'),
    ('09', 'Superior universitaria completa'),
    ('10', 'Superior universitaria incompleta'),
    ('11', 'Sin información'),
    ('12', 'No corresponde (menores de 3 años)'),
)

OCUPACION_CHOICES = (
    ('01', 'Profesional'),
    ('02', 'Empleado'),
    ('03', 'Comerciante'),
    ('04', 'Obrero'),
    ('05', 'Ama casa'),
    ('06', 'Estudiante'),
    ('07', 'Sin ocupacion'),
    ('08', 'Otro'),
)


PARENTESCO_PADRE = '1'

PARENTESCO_MADRE = '2'

PARENTESCO_HERMANOS = '3'

PARENTESCO_OTROS = '4'

PARENTESCO_CHOICES = (
    (PARENTESCO_PADRE, 'Padre'),
    (PARENTESCO_MADRE, 'Madre'),
    (PARENTESCO_HERMANOS, 'Hermanos'),
    (PARENTESCO_OTROS, 'Otros'),
)

PARENTESCO_CHOICES_DICT = {
    PARENTESCO_PADRE: 'Padre',
    PARENTESCO_MADRE: 'Madre',
    PARENTESCO_HERMANOS: 'Hermanos',
    PARENTESCO_OTROS: 'Otros',
}


TIPO_ANTECEDENTE_PERSONAL = '1'

TIPO_ANTECEDENTE_GINECOOBSTETRA = '2'

TIPO_ANTECEDENTE_PATOLOGICO = '3'

TIPO_ANTECEDENTE_PSICOLOGICO = '4'

TIPO_ANTECEDENTE_CHOICES = (
    (TIPO_ANTECEDENTE_PERSONAL, 'Personal'),
    (TIPO_ANTECEDENTE_GINECOOBSTETRA, 'Gineco-Obstetra'),
    (TIPO_ANTECEDENTE_PATOLOGICO, 'Patológico'),
    (TIPO_ANTECEDENTE_PSICOLOGICO, 'Psicológico'),
)


TIPO_INSTEDUC = (
    ('1', 'PRONOEI'),
    ('2', 'Jardín'),
    ('3', 'Colegio'),
    ('4', 'Otro'),
)


NIVEL_INSTEDUC = (
    ('1', 'Inicial'),
    ('2', 'Primaria'),
    ('3', 'Secundaria'),
)


REGISTRO_ANTECEDENTE_NEGATIVO = '0'

REGISTRO_ANTECEDENTE_POSITIVO = '1'

REGISTRO_ANTECEDENTE_NOSABE = '2'

REGISTRO_ANTECEDENTE_CHOICES = (
    (REGISTRO_ANTECEDENTE_NEGATIVO, 'No'),
    (REGISTRO_ANTECEDENTE_POSITIVO, 'Sí'),
    (REGISTRO_ANTECEDENTE_NOSABE, 'No sabe'),
)


GRUPO_ANTECEDENTES_PERSONALES = '1'

GRUPO_ANTECEDENTES_FAMILIARES = '2'

GRUPO_ANTECEDENTES_CHOICES = (
    (GRUPO_ANTECEDENTES_PERSONALES, 'Antecedentes personales'),
    (GRUPO_ANTECEDENTES_FAMILIARES, 'Antecedentes familiares')
)


SUBGRUPO_ANTECEDENTES_PATOLOGICOS = '1'

SUBGRUPO_ANTECEDENTES_LESIONES = '2'

SUBGRUPO_ANTECEDENTES_CANCER = '3'

SUBGRUPO_ANTECEDENTES_MENTAL = '4'

SUBGRUPO_ANTECEDENTES_INTERVENCIONES_QUIRURGICAS = '5'

SUBGRUPO_ANTECEDENTES_CHOICES = (
    (SUBGRUPO_ANTECEDENTES_PATOLOGICOS, 'Patológicos'),
    (SUBGRUPO_ANTECEDENTES_LESIONES, 'Lesiones premalignas'),
    (SUBGRUPO_ANTECEDENTES_CANCER, 'Cáncer'),
    (SUBGRUPO_ANTECEDENTES_MENTAL, 'Salud mental'),
    (SUBGRUPO_ANTECEDENTES_INTERVENCIONES_QUIRURGICAS, 'Intervenciones quirúrgicas'),
)


MESES_LIMITE_CONSULTA_NACIDOS = 1
