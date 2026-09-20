# Quipux Earthquake API

Backend desarrollado para la prueba técnica de Quipux.

La solución consume eventos sísmicos de la API pública de USGS, realiza procesamiento de los datos, los almacena en MongoDB, calcula métricas, genera reportes horarios mediante Apache Airflow y expone la información mediante una API REST desarrollada con FastAPI.

---

## Tecnologías

- Python 3.12
- FastAPI
- Pydantic
- MongoDB
- PyMongo
- Requests
- Apache Airflow
- Docker
- Docker Compose

---

## Arquitectura

La solución está organizada por responsabilidades:

```text
USGS Earthquake API
        |
        | Cada 3 minutos
        v
Servicio de Ingesta
        |
        v
Transformación de datos
        |
        v
MongoDB
   |          |             |
   v          v             v
earthquakes  metrics   hourly_reports
   |          |             ^
   |          |             |
   +----------+-------------+
              |
              v
           FastAPI
              |
       +------+------+------+
       |      |      |      |
       v      v      v      v
 /earthquakes /metrics /reports /health

Apache Airflow
      |
      | Cada hora
      v
Reporte consolidado
      |
      v
MongoDB