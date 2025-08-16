from fastapi import APIRouter, Response
from pydantic import BaseModel
from fastapi.responses import FileResponse
import pandas as pd
from ydata_profiling import ProfileReport
from pathlib import Path

router=APIRouter()

@router.get("/columns-types")
async def get_columns_and_types():
    df = pd.read_csv("uploads/dataset.csv")
    column_types = {}

    for col in df.columns:
        if df[col].dtype in ['int64', 'float64']:
            column_types[col] = 'numerical'
        else:
            column_types[col] = 'categorical'

    return {"columns": column_types}

class NullHandlingRequest(BaseModel):
    column: str
    strategy: str  # depends on column type

@router.post("/handle-nulls")
async def handle_nulls(request: NullHandlingRequest):
    df = pd.read_csv("uploads/dataset.csv")
    col = request.column
    strat = request.strategy.lower()

    print(strat)

    if col not in df.columns:
        return {"error": "Column not found"}

    if df[col].dtype in ['int64', 'float64']:  # Numerical
        if strat == "replace with mean":
            df[col].fillna(df[col].mean(), inplace=True)
        elif strat == "replace with median":
            df[col].fillna(df[col].median(), inplace=True)
        elif strat == "replace with mode":
            df[col].fillna(df[col].mode()[0], inplace=True)
        elif strat == "interpolate":
            df[col].interpolate(method='linear', inplace=True)
        elif strat == "forward fill (ffill)":
            df[col].fillna(method='ffill', inplace=True)
        elif strat == "backward fill (bfill)":
            df[col].fillna(method='bfill', inplace=True)
        elif strat == "zero":
            df[col].fillna(0, inplace=True)
        elif strat == "drop rows":
            df = df[df[col].notna()]
        else:
            return {"error": "Invalid strategy for numerical column"}

    else:  # Categorical
        if strat == "replace with mode":
            df[col].fillna(df[col].mode()[0], inplace=True)
        elif strat == "constant":
            df[col].fillna("Unknown", inplace=True)
        elif strat == "forward fill (ffill)":
            df[col].fillna(method='ffill', inplace=True)
        elif strat == "backward fill (bfill)":
            df[col].fillna(method='bfill', inplace=True)
        elif strat == "drop rows":
            df = df[df[col].notna()]
        else:
            return {"error": "Invalid strategy for categorical column"}

    df.to_csv("uploads/dataset.csv", index=False)
    return {"message": f"Handled nulls in '{col}' using '{strat}' strategy."}

