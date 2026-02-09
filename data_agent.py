import pandas as pd
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Load dataset
file = input("Enter CSV path: ")
df = pd.read_csv(file)

print("\nColumns found:", list(df.columns))

question = input("\nAsk about the data: ")

prompt = f"""
You are a Python pandas expert.

Data columns: {list(df.columns)}

User question: {question}

Write ONLY executable Python code.

Rules:
- Use dataframe df
- Use pandas only
- Final answer must be stored in variable result
- Do NOT explain
- Do NOT include markdown
- Do NOT include comments
Return only pure Python code.
"""


response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": prompt}]
)

code = response.choices[0].message.content

# Remove markdown formatting if present
if "```" in code:
    code = code.split("```")[1]
    if code.startswith("python"):
        code = code[len("python"):]

code = code.strip()

print("\nAI generated code:\n")
print(code)

try:
    local_vars = {"df": df}
    exec(code, {}, local_vars)
    result = local_vars.get("result", "No result variable produced")
except Exception as e:
    result = f"Execution error: {str(e)}"

explain = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": "Explain the result simply"},
        {"role": "user", "content": str(result)}
    ]
)

print("\nAnswer:")
print(explain.choices[0].message.content)
