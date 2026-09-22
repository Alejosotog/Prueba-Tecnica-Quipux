from prometheus_client import Counter, Histogram, Gauge


# Total de eventos recibidos desde la API de USGS
ingestion_events_received = Counter(
    "earthquake_ingestion_events_received_total",
    "Total de eventos sísmicos recibidos desde USGS"
)


# Total de eventos nuevos almacenados en MongoDB
ingestion_events_new = Counter(
    "earthquake_ingestion_events_new_total",
    "Total de eventos sísmicos nuevos almacenados"
)


# Total de errores durante la ingesta
ingestion_errors = Counter(
    "earthquake_ingestion_errors_total",
    "Total de errores durante la ingesta"
)


# Duración de cada proceso de ingesta
ingestion_duration = Histogram(
    "earthquake_ingestion_duration_seconds",
    "Duración del proceso de ingesta en segundos"
)


# Total de eventos actualmente almacenados
stored_earthquakes = Gauge(
    "earthquake_stored_events",
    "Cantidad actual de eventos sísmicos almacenados"
)
