import google.generativeai as genai
from fastapi import APIRouter
from pathlib import Path
from dotenv import load_dotenv
import json, csv, os


router = APIRouter()

env_path = Path(__file__).resolve().parent.parent / "config.env"


load_dotenv(dotenv_path=env_path)

UPLOAD_DIR = Path("uploads")
API_DIR= Path("Gemini_API_data")

# Set your Gemini API key
GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

#Extracts text from a PDF file using PyMuPDF (fitz)
def extract_text_from_csv() -> str:
    doc_path= UPLOAD_DIR / "documentation.csv"
    text_data = []
    
    with open(doc_path, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            text_data.append(" ".join(row))  # Join columns with space
    
    return text_data



@router.get("/generate-questions")
async def generate_business_questions():
    doc_text = extract_text_from_csv()
    
    if not doc_text:
        return {"error": "Documentation file not found"}
    
    # print(doc_text)

    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""
    Given the uploaded dataset documentation containing customer information for a company, identify and provide business-related insights regarding the relationships between the columns. 

    ### **Instructions:**
    - The output should be a **list of relationships** between the dataset columns.
    - Instead of column numbers, **use actual column names** from the dataset.
    - Focus on identifying **churn-related insights**, but also include general **business insights** between features such as customer demographics, orders, satisfaction, and behavior.
    - Do not provide explanations or questions—just structured insights.

    ### **Output Format:**
    Provide the output in the exact format below:

    Column1 Name: Column2 Name : Insight

    For example:

    SatisfactionScore: Churn : Higher satisfaction leads to lower churn.
    OrderCount: Churn : More orders indicate lower churn.
    CashbackAmount: Churn : Higher cashback leads to lower churn risk.
    Complaint: Churn : More complaints result in higher churn.
    OrderAmountHikeFromLastYear: Churn : A sharp increase or decrease may indicate churn risk.
    PreferredLoginDevice: Churn : Some devices may have higher churn rates.

    Dataset Documentation:
    {doc_text}

    Provide **ONLY** the structured output as described. Do **NOT** include explanations, questions, or column numbers.
    """


    response = model.generate_content(prompt)

    questions = response.text.split("\n")

    actual_questions=[]

    column_relations = {}

    counter=0
    for que in questions:
        if(que.__contains__(":")):
            # print(que)
            l1 = que.split(":")
            column_relations[f"Q{counter})"] = [f"{l1[0]}:{l1[1]}"]

            if(l1[2]=="insight"):
                actual_questions.append("Q"+str(counter)+") :"+l1[3])
            else:    
                actual_questions.append("Q"+str(counter)+") :"+l1[2])

            counter+=1

    
    # Save column relationships to a JSON file
    json_path = API_DIR / "column_relationships.json"
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(column_relations, json_file, indent=4)

    return {"questions": actual_questions}