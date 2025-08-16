from fastapi import APIRouter, File, UploadFile
from pathlib import Path
import fitz
import csv
import pandas as pd

router=APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

async def save_dataset(dataset: UploadFile,dataset_path: Path):

    content= await dataset.read()

    if dataset.filename.endswith(".xlsx"):
        # Convert XLSX to CSV
        df = pd.read_excel(content)
        df.to_csv(dataset_path, index=False)

    elif dataset.filename.endswith(".json"):
        # Convert JSON to CSV
        df = pd.read_json(content)
        df.to_csv(dataset_path, index=False)

    elif dataset.filename.endswith(".csv"):
        dataset_path.write_bytes(content)


    
    


async def save_document(document: UploadFile,document_path: Path):

    ext = document.filename.split(".")[-1].lower()
    contents = await document.read()

    if ext in ["xls", "xlsx"]:
        # Convert Excel file to CSV
        df = pd.read_excel(document.file)
        df.to_csv(document_path, index=False)

    elif ext == "csv":
        # Save CSV file directly
        with document_path.open("wb") as f:
            f.write(contents)

    elif ext == "pdf":
        # Convert PDF to CSV using PyMuPDF (fitz)
        with fitz.open(stream=contents, filetype="pdf") as doc:
            text_lines = [page.get_text("text").split("\n") for page in doc]

        text_lines = [line for page in text_lines for line in page if line.strip()]

        with document_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            for line in text_lines:
                writer.writerow([line])
    
    
    

@router.post("")
async def upload(dataset: UploadFile = File(...), documentation: UploadFile = File(...)):
    dataset_path = UPLOAD_DIR / "dataset.csv"  # Fixed dataset filename
    doc_path = UPLOAD_DIR / "documentation.csv"  # Fixed documentation filename


    dataset_acceptable_formats= [".xls", ".xlsx", ".csv", ".json"]
    dataset_documentation_acceptable_formats= [".xls", ".xlsx", ".csv", ".json", ".txt", ".pdf", ".html"]

    if (not any(dataset.filename.endswith(ext) for ext in dataset_acceptable_formats) or not any(documentation.filename.endswith(ext) for ext in dataset_documentation_acceptable_formats)):
        return {"message": "File type is not supported"}


    await save_dataset(dataset=dataset,dataset_path=dataset_path)
    await save_document(document=documentation,document_path=doc_path)


    return {"message": "Files uploaded successfully"}
