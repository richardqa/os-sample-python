# Instalación:

- Instalar pip y virtualenv `sudo apt-get install python-pip python-virtualenv`
- Crear entorno virtual: `virtualenv --no-site-package --distribute`
- Activar el entorno virtual: `source bin/activate`
- Instalar dependencias: `pip install -r requirements/prod.txt`

El sistema usa datos geoespaciales, por lo que es necesario tener instalado [**PostGIS**](https://postgis.net/install/)
junto a la base de datos (que debe ser **PostgreSQL**), para activar la extensión PostGIS ejecutar en la base de datos 
de MPI:

```sql
CREATE EXTENSION postgis;
```

si la extensión ya fue creada anteriormente, se puede actualizar con:
```sql
ALTER EXTENSION postgis UPDATE;
```

- Cargar fixtures:

```sh
./manage.py loaddata phr/catalogo/fixtures/catalogo.json
./manage.py loaddata phr/ubigeo/fixtures/ubigeo.json
./manage.py loaddata phr/establecimiento/fixtures/sectores.json
./manage.py loaddata phr/establecimiento/fixtures/establecimiento.json
./manage.py loaddata phr/insteducativa/fixtures/insteducativa.json
./manage.py loaddata phr/catalogo/fixtures/familiamedicamento.json
./manage.py loaddata phr/catalogo/fixtures/medicamento.json
```


Configuración de variables de entorno:
--

* `SECRET_KEY` Secret Key de Django.
* `ALLOWED_HOSTS` Lista de dominios permitidos para acceder a la aplicación.
* `DB_NAME` Nombre de la base de datos.
* `DB_USER` Usuario de la base de datos.
* `DB_PASSWORD` Contraseña del usuario de la base de datos.
* `DB_HOST` Servidor de base de datos.
* `DB_PORT` Puerto de la base de datos.
* `APP_IDENTIFIER` Identificador de la aplicación.
* `HIDE_DRFDOCS` Mostrar documentación de DRF `(1/0)`.
* `MPI_CENTRAL_HOST` Host de MPI Central, para realizar consulta de ciudadanos
* `MPI_CENTRAL_TOKEN` Token de conexión a MPI Central
* `ACTUALIZAR_DATOS_RENIEC_CADA_DIAS` Tiempo en **días** para volver a obtener datos de ciudadano desde RENIEC y 
  actualizar información almacenada en base de datos local.


Luego de desplegar el proyecto, dentro del administrador del sistema `/admin` se debe crear una `Configuración de conexión a Internet` para que el sistema tenga conexión a RENIEC, SIS y Migraciones.

---

MINSA (c) 2016
