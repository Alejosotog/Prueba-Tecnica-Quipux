from services.ingestion_service import ingest_earthquakes


total = ingest_earthquakes()

print("Eventos procesados:", total)