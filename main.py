from fastapi import FastAPI, UploadFile, File
import pandas as pd
import os

app = FastAPI()

DATA_PATH = "data/sales.csv"


# 1. Test route
@app.get("/")
def home():
    return {"message": "AI Engineer API is running 🚀"}


# 2. Upload CSV
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    os.makedirs("data", exist_ok=True)

    with open(DATA_PATH, "wb") as f:
        f.write(await file.read())

    df = pd.read_csv(DATA_PATH)
    return {"rows": len(df), "columns": list(df.columns)}


# 3. View all sales
@app.get("/sales")
def get_sales(product: str = None):
    if not os.path.exists(DATA_PATH):
        return {"error": "Upload a file first"}

    df = pd.read_csv(DATA_PATH)

    if product:
        df = df[df["product"] == product]

    return df.to_dict(orient="records")


# 4. Calculate revenue
@app.get("/revenue")
def revenue():
    if not os.path.exists(DATA_PATH):
        return {"error": "Upload a file first"}

    df = pd.read_csv(DATA_PATH)
    total = (df["price"] * df["quantity"]).sum()

    return {"total_revenue": float(total)}
