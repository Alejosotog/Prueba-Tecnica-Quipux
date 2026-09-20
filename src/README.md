# Quipux Earthquake API

## Descripcion

Backend para consumir eventos sismicos de USGS, procesarlos, almacenarlos en MongoDB y exponerlos mediante una API REST con FastAPI.

## Tecnologias

- Python 3.12
- FastAPI
- Pydantic
- MongoDB
- PyMongo
- Requests
- Apache Airflow
- Docker
- Docker Compose

## Componentes

- USGS: fuente de eventos sismicos.
- Servicio de ingesta: consulta USGS cada 3 minutos.
- MongoDB: almacenamiento de eventos, metricas y reportes.
- FastAPI: API REST.
- Airflow: generacion de reportes horarios.
- Docker Compose: orquestacion de servicios.

## Ejecucion

Desde la carpeta src:

    docker compose up -d --build

## Documentacion API

Swagger:

    http://localhost:8000/docs

Health check:

    GET /health

Eventos:

    GET /earthquakes/

Metricas:

    GET /metrics/

Reportes:

    GET /reports/

## Funcionalidades

### Eventos

- Filtrado por magnitud minima y maxima.
- Paginacion.
- Ordenamiento.
- Validacion de parametros.

### Ingestion

El servicio consulta la API de USGS cada 3 minutos.

Los eventos se identifican mediante event_id y se almacenan mediante upsert para evitar duplicados.

### Metricas

- Cantidad de terremotos de la ultima hora.
- Magnitud promedio.
- Magnitud maxima.

### Reportes

Los reportes horarios se almacenan en la coleccion hourly_reports.

### Airflow

DAG:

    airflow/dags/earthquake_hourly_report.py

El DAG genera un reporte consolidado cada hora.

## Variables de entorno

    MONGO_URI
    DATABASE_NAME

En Docker:

    MONGO_URI=mongodb://mongodb:27017
    DATABASE_NAME=earthquake_db

## Estructura

    api/
    clients/
    database/
    models/
    services/
    utils/
    airflow/
    Dockerfile
    docker-compose.yml
    requirements.txt
    postman_collection.json
    architecture.md
    README.md
