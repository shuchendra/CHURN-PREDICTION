from fastapi import APIRouter
from pathlib import Path
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
import os, base64
from .graphs import bar_chart_single_column, pie_chart_single_column, histogram_single_column, box_plot_single_column, density_plot_single_column, mosaic_plot_relationship, stacked_bar_chart_relationship, box_plot_relationship, violin_plot_relationship, bar_chart_relationship, scatter_plot_relationship, line_plot_relationship, heatmap_relationship

Gemini_API_data=Path("gemini_API_data")
UPLOAD_DIR=Path("uploads")
GRAPHS_DIR = Path("graphs")

router = APIRouter()

env_path = Path(__file__).resolve().parent.parent / "config.env"
load_dotenv(dotenv_path=env_path)

# Set your Gemini API key
GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)



def get_column_details(df: pd.DataFrame, col: str):

    total_values=len(df[col])
    json = {}
    
    json["name"] = col
    if(df[col].nunique()/total_values < 0.05):
        json["data_type"]="categorical"
    else:
        json["data_type"]="numerical"

    json["unique_values"]=df[col].nunique()

    json["possible_visualizations"]=["Histogram", "Box Plot", "Scatter Plot", "Bar Chart", "Pie Chart", "Line Plot", "Heat Map", "Violin Plot", "Mosiac Plot", "Stacked Bar Chart", "Density Plots"]

    return json




def modify_columns(actual_visualizations: dict, name: str):
    s=actual_visualizations[name].strip()[1:-1].split('"')
    l1=[]
    for i in s:
        if(len(i)>2):
            l1.append(i)
    return l1

# Function to encode images
def encode_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except FileNotFoundError:
        # print(f"File not found: {image_path}")
        return None
    
def get_details(s: str):
    l1=[]
    l1.append(s[(s.index("relationship_status")+len("relationship_status")+4):(s.index(",")-1)])
    l1.append(s[(s.index("explanation")+len("explanation")+4):-18])
    return l1

@router.get("/{index}")
async def create_visualization(index : str):

    json1 = pd.read_json("Gemini_API_data/column_relationships.json")

    columns = json1[index][0]
    df = pd.read_csv("uploads/dataset.csv")

    column1 = get_column_details(df, columns.split(":")[0].strip())
    column2 = get_column_details(df, columns.split(":")[1].strip())

    column_details = {}
    column_details["column1"] = column1
    column_details["column2"] = column2

    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    You are a data visualization expert. Given the metadata of two dataset columns, your task is to determine the most suitable visualization(s) to explore the relationship between them.  

    ## **Instructions**:
    - The input consists of two columns with details including **name, data type, unique value count, and possible visualizations**.
    - Your response must be in **JSON format**, where each column is mapped to the most suitable visualization(s) from the given options.
    - Consider the following rules while selecting visualizations:
    - **For Numerical vs. Numerical**: Use **Scatter Plot, Line Plot, or Heatmap** (for correlations).
    - **For Numerical vs. Categorical**: Use **Box Plot, Violin Plot, or Bar Chart**.
    - **For Categorical vs. Categorical**: Use **Bar Chart, Mosaic Plot, or Stacked Bar Chart**.
    - **If unique values are many**: Avoid Pie Charts and prefer **Histograms or Density Plots**.
    - **If unique values are few**: Pie Charts, Bar Charts, or Count Plots are effective.
    - Do NOT suggest visualizations that are not in the "possible_visualizations" list.

    columns_details:
    {column_details}

    output format:
    column1: [visulization(s)]
    column2: [visualization(s)]
    realationship: [visulization(s)]

    The response should strictly follow the output format, I only want the reponse to consists of those 3 variables
    """

    response = model.generate_content(prompt)
    visualizations = response.text.split("\n")
    visualizations = visualizations[visualizations.index('{')+1:visualizations.index('}')]
    # print(visualizations)

    actual_visualizations={}
    actual_visualizations["column1"] = visualizations[0].split(":")[1][0:-1].strip()
    actual_visualizations["column2"] = visualizations[1].split(":")[1][0:-1].strip()
    actual_visualizations["relationships"] = visualizations[2].split(":")[1].strip()

    # print(actual_visualizations)

    actual_visualizations["column1"] = modify_columns(actual_visualizations=actual_visualizations, name="column1")
    actual_visualizations["column2"] = modify_columns(actual_visualizations=actual_visualizations, name="column2")
    actual_visualizations["relationships"] = modify_columns(actual_visualizations=actual_visualizations, name="relationships")

    column1_name = columns.split(":")[0].strip()
    column2_name = columns.split(":")[1].strip()

    column1_image_paths = []
    column2_image_paths = []

    for i in actual_visualizations["column1"]:
        if (i=="Bar Chart"):
            column1_image_paths.append(f"{column1_name}_bar_chart.png")
            bar_chart_single_column(df=df, col=column1_name)
        if(i=="Pie Chart"):
            column1_image_paths.append(f"{column1_name}_pie_chart.png")
            pie_chart_single_column(df=df, col=column1_name)
        if(i=="Histogram"):
            column1_image_paths.append(f"{column1_name}_histogram.png")
            histogram_single_column(df=df, col=column1_name)
        if(i=="Box Plot"):
            column1_image_paths.append(f"{column1_name}_box_plot.png")
            box_plot_single_column(df=df, col=column1_name)
        if(i=="Density Plots"):
            column1_image_paths.append(f"{column1_name}_density_plot.png")
            density_plot_single_column(df=df, col=column1_name)

    for i in actual_visualizations["column2"]:
        if (i=="Bar Chart"):
            column2_image_paths.append(f"{column2_name}_bar_chart.png")
            bar_chart_single_column(df=df, col=column2_name)
        if(i=="Pie Chart"):
            column2_image_paths.append(f"{column2_name}_pie_chart.png")
            pie_chart_single_column(df=df, col=column2_name)
        if(i=="Histogram"):
            column2_image_paths.append(f"{column2_name}_histogram.png")
            histogram_single_column(df=df, col=column2_name)
        if(i=="Box Plot"):
            column2_image_paths.append(f"{column2_name}_box_plot.png")
            box_plot_single_column(df=df, col=column2_name)
        if(i=="Density Plots"):
            column2_image_paths.append(f"{column2_name}_density_plot.png")
            density_plot_single_column(df=df, col=column2_name)

    for i in actual_visualizations["relationships"]:
        if(i=="Mosiac Plot" or i=="Mosaic Plot"):
            mosaic_plot_relationship(df=df, col1=column1_name, col2=column2_name)
        if(i=="Stacked Bar Chart"):
            stacked_bar_chart_relationship(df=df, col1=column1_name, col2=column2_name)
        if(i=="Box Plot"):
            box_plot_relationship(df=df, col1=column1_name, col2=column2_name)
        if(i=="Violin Plot"):
            violin_plot_relationship(df=df, col1=column1_name, col2=column2_name)
        if(i=="Bar Chart"):
            bar_chart_relationship(df=df, col1=column1_name, col2=column2_name)
        if(i=="Scatter Plot"):
            scatter_plot_relationship(df=df, col1=column1_name,col2= column2_name)
        if(i=="Line Plot"):
            line_plot_relationship(df=df, col1=column1_name, col2=column2_name)
        if(i=="Heat Map"):
            heatmap_relationship(df=df, col1=column1_name, col2=column2_name)

    relationships_names=[]

    for i in actual_visualizations["relationships"]:
        if i=="Mosiac Plot":
            s2="Mosaic Plot"
            s1 = s2.lower()
            s1 = s1.replace(" ","_")
            s = column1_name+"_"+column2_name+"_"+s1+".png"
            relationships_names.append(s)
        elif i=="Mosaic Plot":
            s2="Mosiac Plot"
            s1 = s2.lower()
            s1 = s1.replace(" ","_")
            s = column1_name+"_"+column2_name+"_"+s1+".png"
            relationships_names.append(s)
        s1 = i.lower()
        s1 = s1.replace(" ","_")
        s = column1_name+"_"+column2_name+"_"+s1+".png"
        relationships_names.append(s)
        
    # Create a list of full image paths for the LLM request
    image_paths = []

    for name in relationships_names:
        file_path = GRAPHS_DIR / name  # Construct the full path
        # print(file_path, file_path.exists())
        if file_path.exists():  
            image_paths.append(str(file_path.resolve().as_posix()))


    # print(image_paths)
    
    res={}

    res[column1_name] = column1_image_paths
    res[column2_name] = column2_image_paths

    temp = {}
    # Encode and add images to the request
    for img_path in image_paths:

        graph_details = {}

        encoded_image = encode_image(img_path)
        type_of_graph=""
        if img_path.__contains__("mosaic_plot"):
            type_of_graph="Mosiac Plot"
        if(img_path.__contains__("stacked_bar_chart")):
            type_of_graph="Stacker Bar Chart"
        if(img_path.__contains__("violin_plot")):
            type_of_graph="Violin Plot"
        if(img_path.__contains__("bar_chart")):
            type_of_graph="Bar Chart"
        if(img_path.__contains__("scatter_plot")):
            type_of_graph="Scatter Plot"
        if(img_path.__contains__("line_plot")):
            type_of_graph="Line Plot"
        if(img_path.__contains__("heatmap")):
            type_of_graph="Heat Map"


        s = str(img_path)

        graph_details["image"] = s[s.rindex("/")+1:]

        # print(type(img_path) , type(s), s)

        # print(s.rindex["/"])

        # graph_details["image"] = "temporary"

        prompt = f"""
        You are an expert in data analysis. Analyze the relationships between the two features shown in the attached visualizations. Determine whether they are strongly related, weakly related, or not related at all. Provide a detailed explanation for your conclusion.

        ### Output Format:
            "relationships_analysis": [
                [   
                    "relationship_status": "<Strong / Weak / No Relationship>",
                    "explanation": "<Detailed reasoning>"
                ]
            ]

        image details:
        {encoded_image}
        column1_name:
        {column1_name}
        column2_name:
        {column2_name}
        type of graph:
        {type_of_graph}
        """

        response = model.generate_content(prompt)

        relationship_analysis={}

        response_text = str(response.text)

        l1 = get_details(response_text)

        relationship_analysis["relationships_analysis"] = l1[0]
        relationship_analysis["explanation"] = l1[1]

        graph_details["relationship_analysis"] = relationship_analysis
        temp[type_of_graph] = graph_details

    res["relationship"] = temp
                

    return {"visualizations": res}

