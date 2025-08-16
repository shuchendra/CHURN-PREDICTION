from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import upload, generate_questions, dataset_info, create_visualization, perform_EDA
from fastapi.middleware.cors import CORSMiddleware


# pip freeze > requirements.txt

app=FastAPI()

GRAPH_FOLDER = "graphs"


# Mount the "graphs" folder to serve images
app.mount("/graphs", StaticFiles(directory=GRAPH_FOLDER), name="graphs")

# for allowing frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(upload.router, prefix="/upload", tags=['Uploads'])
app.include_router(generate_questions.router, prefix="/documentation", tags=['Generate-Questions'])
app.include_router(dataset_info.router, prefix="/dataset", tags=['Dataset-Info'])
app.include_router(create_visualization.router, prefix="/create-visualization", tags=['Creating-Visualization'])
app.include_router(perform_EDA.router, prefix="/eda", tags=["Performing EDA"])

@app.get("/")
async def main():
    return "Hello World!!"