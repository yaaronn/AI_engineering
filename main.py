from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI()
templates = Jinja2Templates(directory="templates")

DATA_PATH = "data/uploaded.csv"

chat_memory = []

@app.get("/chat", response_class=HTMLResponse)
def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@app.post("/upload", response_class=HTMLResponse)
async def upload_file(request: Request, file: UploadFile = File(...)):
    os.makedirs("data", exist_ok=True)

    with open(DATA_PATH, "wb") as f:
        f.write(await file.read())

    return templates.TemplateResponse(
        "chat.html",
        {"request": request, "answer": "File uploaded successfully! Ask a question."}
    )


@app.post("/ask", response_class=HTMLResponse)
async def ask_question(request: Request, question: str = Form(...)):
    global chat_memory

    if not os.path.exists(DATA_PATH):
        return templates.TemplateResponse(
            "chat.html",
            {"request": request, "answer": "Upload a dataset first."}
        )

    df = pd.read_csv(DATA_PATH)

    # store user message
    #chat_memory.append({"role": "user", "content": question})

    messages = [
    {
        "role": "system",
        "content": f"""
You are a Python pandas data analyst.

You must write executable Python code only.

Rules:
- dataframe name is df
- columns are {list(df.columns)}
- final output must be stored in variable 'result'
- no explanations
- no conversation
- no markdown
"""
    }
] + chat_memory


    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )

    code = response.choices[0].message.content

    # remove markdown
    if "```" in code:
        code = code.split("```")[1]
        if code.startswith("python"):
            code = code[len("python"):]

    code = code.strip()

    try:
        local_vars = {"df": df}
        exec(code, {}, local_vars)
        result = local_vars.get("result", "No result produced")
    except Exception as e:
        result = f"Execution error: {str(e)}"

    explain = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Explain simply"},
            {"role": "user", "content": str(result)}
        ]
    )

    answer = explain.choices[0].message.content

    # store AI reply
    chat_memory.append({"role": "assistant", "content": answer})

    return templates.TemplateResponse(
        "chat.html",
        {"request": request, "answer": answer}
    )

