# Arquitectura de la solucion

USGS Earthquake API
        |
        | Cada 3 minutos
        v
Servicio de Ingesta
        |
        v
MongoDB
   |       |       |
   v       v       v
earthquakes metrics hourly_reports
   |       |       |
   +-------+-------+
           |
           v
        FastAPI
           |
           +-- /earthquakes/
           +-- /metrics/
           +-- /reports/
           +-- /health

Airflow
   |
   | Cada hora
   v
Reporte consolidado
   |
   v
MongoDB / hourly_reports

Docker Compose
   |
   +-- MongoDB
   +-- FastAPI
   +-- Ingestion
