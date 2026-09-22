# Prueba Técnica Quipux
# John Alejandro Soto Gomez. 
## Líder Técnico de Ingeniería de Datos y Desarrollo Python

Solución desarrollada para la prueba técnica del proceso de selección de Quipux.

El proyecto implementa una solución backend para consumir eventos sísmicos desde la API pública de USGS, procesarlos, almacenarlos en MongoDB, calcular métricas, exponer información mediante una API REST y generar reportes consolidados mediante Apache Airflow.

Adicionalmente, la solución incorpora RabbitMQ para mensajería, Prometheus y Grafana para observabilidad y un mecanismo de cache temporal para optimizar consultas de métricas.

---

## 2. Tecnologías

- Python
- FastAPI
- Pydantic
- MongoDB
- PyMongo
- Requests
- Apache Airflow
- RabbitMQ
- Pika
- Prometheus
- Grafana
- Docker
- Docker Compose
- Postman


---

### 3. Arquitectura

La solución está organizada en diferentes capas y servicios.

```text
                         ┌───────────────────┐
                         │    API pública    │
                         │       USGS        │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │    USGS Client    │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │ Ingestion Service │
                         └─────────┬─────────┘
                                   │
                         ┌─────────┴─────────┐
                         │                   │
                         ▼                   ▼
                   ┌───────────┐       ┌───────────┐
                   │  MongoDB  │       │ RabbitMQ  │
                   └─────┬─────┘       └─────┬─────┘
                         │                   │
                         │                   ▼
                         │            ┌───────────────┐
                         │            │Event Processor│
                         │            └───────────────┘
                         │
              ┌──────────┴──────────┐
              │                     │
              ▼                     ▼
        ┌───────────┐          ┌───────────┐
        │  FastAPI  │          │  Airflow  │
        └─────┬─────┘          └─────┬─────┘
              │                      │
              │                      ▼
              │                 Reporte horario
              │                      │
              └──────────┬───────────┘
                         ▼
                     MongoDB

FastAPI / Ingestion
        │
        ▼
   Prometheus
        │
        ▼
     Grafana
```


---

## 4. Estructura del proyecto

```text
Prueba_tecnica_quipux/
│
├── README.md
├── ARQUITECTURA.docx
├── docker-compose.yml
├── prometheus.yml
│
└── src/
    │
    ├── api/
    │   ├── main.py
    │   └── routes/
    │       ├── earthquakes.py
    │       ├── metrics.py
    │       └── reports.py
    │
    ├── clients/
    │   └── usgs_client.py
    │
    ├── database/
    │   ├── connection.py
    │   ├── earthquake_repository.py
    │   ├── metrics_repository.py
    │   └── reports_repository.py
    │
    ├── models/
    │   ├── earthquake.py
    │   └── earthquake_query.py
    │
    ├── services/
    │   ├── ingestion_runner.py
    │   ├── ingestion_service.py
    │   ├── metrics_service.py
    │   └── report_service.py
    │
    ├── utils/
    │   ├── cache.py
    │   ├── prometheus_metrics.py
    │   └── transformers.py
    │
    ├── messaging/
    │   ├── rabbitmq_consumer.py
    │   └── rabbitmq_producer.py
    │
    ├── airflow/
    │   └── dags/
    │       └── earthquake_hourly_report.py
    │
    ├── config.py
    ├── Dockerfile
    ├── requirements.txt
    ├── architecture.md
    └── postman_collection.json
```

---

## 5. Flujo de ingesta

La ingesta se ejecuta aproximadamente cada tres minutos.

```text
USGS
  ↓
USGS Client
  ↓
Ingestion Service
  ↓
Transformación
  ↓
Detección de nuevos eventos
  ↓
MongoDB
  ↓
RabbitMQ
```

Durante el proceso se registran eventos relevantes y errores de ejecución.

Los eventos existentes no se vuelven a insertar.

---

## 6. Persistencia

La solución utiliza MongoDB.

Base de datos:

```text
earthquake_db
```

Colecciones principales:

```text
earthquakes
metrics
hourly_reports
```

### earthquakes

Almacena los eventos sísmicos obtenidos desde USGS.

### metrics

Almacena las métricas calculadas.

### hourly_reports

Almacena los reportes horarios generados por Airflow.

---

## 7. Métricas

El sistema calcula:

- Cantidad de eventos.
- Cantidad de eventos por hora.
- Magnitud promedio.
- Magnitud máxima.
- Distribución de magnitudes por rangos.

La lógica se encuentra en:

```text
src/services/metrics_service.py
```

---

## 8. API REST

La API está desarrollada con FastAPI.

URL base:

```text
http://localhost:8000
```

### Health check

```http
GET /health
```

Permite verificar la disponibilidad de la API.

### Eventos sísmicos

```http
GET /earthquakes/
```

Permite:

- Consultar eventos.
- Filtrar por magnitud.
- Paginar.
- Ordenar resultados.

Ejemplo:

```text
GET /earthquakes/?page=1&page_size=10
```

### Métricas

```http
GET /metrics/
```

Retorna las métricas calculadas.

La respuesta utiliza cache temporal para reducir consultas repetitivas durante el período de validez de la cache.

### Reportes

```http
GET /reports/
```

Permite consultar los reportes horarios almacenados.

### Métricas de Prometheus

```http
GET /prometheus
```

Expone las métricas de la aplicación para Prometheus.

---

## 9. Validación con Pydantic

La aplicación utiliza Pydantic para validar parámetros de consulta.

Entre las validaciones implementadas:

- Página.
- Tamaño de página.
- Magnitud mínima.
- Magnitud máxima.
- Campo de ordenamiento.
- Dirección del ordenamiento.
- Consistencia entre magnitud mínima y máxima.

Los errores de validación son manejados mediante las respuestas estándar de FastAPI.

---

## 10. RabbitMQ

RabbitMQ se utiliza para desacoplar la publicación de eventos sísmicos del procesamiento posterior.

### Productor

```text
src/messaging/rabbitmq_producer.py
```

Publica los eventos nuevos en:

```text
earthquake.events
```

Exchange:

```text
fanout
```

### Consumidor

```text
src/messaging/rabbitmq_consumer.py
```

Consume los mensajes mediante la cola:

```text
earthquake_events
```

Flujo:

```text
Ingestion
   ↓
RabbitMQ
   ↓
earthquake.events
   ↓
earthquake_events
   ↓
Event Processor
```

El consumidor incluye reintentos de conexión para soportar el inicio coordinado de los contenedores.

---

## 11. Airflow

Apache Airflow genera el reporte consolidado cada hora.

DAG:

```text
earthquake_hourly_report
```

Ubicación:

```text
src/airflow/dags/earthquake_hourly_report.py
```

Flujo:

```text
Airflow
   ↓
Eventos almacenados
   ↓
Procesamiento del reporte
   ↓
Métricas consolidadas
   ↓
MongoDB
```

Los reportes se almacenan en:

```text
hourly_reports
```

---

## 12. Observabilidad

La solución incorpora Prometheus y Grafana.

### Prometheus

Configuración:

```text
prometheus.yml
```

Prometheus recopila métricas de:

- API.
- Servicio de ingesta.

Entre las métricas disponibles se encuentran:

- Eventos recibidos.
- Eventos nuevos.
- Errores de ingesta.
- Duración de operaciones.
- Eventos almacenados.

### Grafana

Grafana permite visualizar las métricas recopiladas por Prometheus mediante dashboards.

Puertos:

```text
Prometheus:  http://localhost:9090
Grafana:     http://localhost:3000
```

---

## 13. Docker Compose

La solución está preparada para ejecutarse mediante Docker Compose.

Servicios:

```text
mongodb
rabbitmq
api
ingestion
event_processor
airflow
prometheus
grafana
```

Puertos principales:

```text
MongoDB       27017
RabbitMQ      5672
RabbitMQ UI   15672
FastAPI       8000
Prometheus    9090
Grafana       3000
```

---

## 14. Ejecución

### Requisitos

Se requiere:

- Docker Desktop.
- Docker Compose.
- Git.

No es necesario instalar MongoDB, RabbitMQ, Airflow o Grafana localmente.

### Iniciar la solución

Desde la raíz del proyecto:

```bash
docker compose up -d --build
```

Verificar los servicios:

```bash
docker compose ps
```

---

## 15. Ver logs

### API

```bash
docker compose logs -f api
```

### Ingesta

```bash
docker compose logs -f ingestion
```

### RabbitMQ / Event Processor

```bash
docker compose logs -f event_processor
```

### Airflow

```bash
docker compose logs -f airflow
```

---

## 16. Detener la solución

```bash
docker compose down
```

Para eliminar también los volúmenes:

```bash
docker compose down -v
```

> El segundo comando elimina los datos persistidos de MongoDB y Grafana.

---

## 17. Postman

Se incluye una colección de Postman:

```text
src/postman_collection.json
```

Esta colección permite probar los principales endpoints de la API.

---

## 18. Documentación adicional

### Arquitectura

```text
src/architecture.md
```

### Diagrama de arquitectura

```text
ARQUITECTURA.docx
```

### Colección Postman

```text
src/postman_collection.json
```

---

## 19. Separación de responsabilidades

La solución está organizada por capas:

```text
Clients
   ↓
Services
   ↓
Repositories
   ↓
MongoDB
```

La API utiliza:

```text
Routes
   ↓
Services
   ↓
Repositories
   ↓
MongoDB
```