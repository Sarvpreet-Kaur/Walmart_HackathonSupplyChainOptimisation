from fastapi import FastAPI,UploadFile, File,Form
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
from forecast_pipeline import forecast_for_product

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/forecast/")

async def forecast_endpoint(
    file: UploadFile = File(...),
    product_name: str = Form(...),
    forecast_days: int = Form(...),
    current_stock: int = Form(...)
):
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
        df['Date'] = pd.to_datetime(df['Date'],dayfirst=True)
        
        result = forecast_for_product(df,product_name,forecast_days,current_stock)
        return result
    except Exception as e:
        return{
            "error":f"Internal error{str(e)}"
        }