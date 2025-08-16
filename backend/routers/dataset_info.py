from fastapi import APIRouter, Response
from fastapi.responses import FileResponse
import pandas as pd
from ydata_profiling import ProfileReport
from pathlib import Path

router=APIRouter()

UPLOAD_DIR = Path("uploads")

@router.get("/info")
async def dataset_info():

    df=pd.read_csv("uploads/dataset.csv")

    # Generate dataset report
    report = ProfileReport(df, explorative=True)
    report_path = UPLOAD_DIR / "report.html"
    report.to_file(report_path)

    if not report_path.exists():
        return {"error": "Report not found. Try regenerating it."}

    return FileResponse(
        path=report_path,
        media_type="text/html",
        filename="dataset_report.html"
    )