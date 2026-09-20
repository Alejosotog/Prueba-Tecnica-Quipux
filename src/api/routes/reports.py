from fastapi import APIRouter

from database.reports_repository import get_reports


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/")
def get_hourly_reports():
    reports = get_reports()

    for report in reports:
        report["_id"] = str(report["_id"])

    return {
        "total": len(reports),
        "data": reports
    }