import requests
import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

question = input("Ask about your sales data: ")

prompt = f"""
You are a data assistant.

Convert user question into JSON.

Rules:
- If asking total revenue → endpoint = revenue
- If asking about a product → endpoint = product_revenue and extract product name

Return ONLY JSON.

Examples:

Question: total revenue
{{"endpoint":"revenue"}}

Question: apple revenue
{{"endpoint":"product_revenue","product":"apple"}}

User question: {question}
"""

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": prompt}]
)

decision_text = response.choices[0].message.content
print("AI decision:", decision_text)

decision = json.loads(decision_text)

# Call correct API
if decision["endpoint"] == "revenue":
    url = "http://127.0.0.1:8000/revenue"

elif decision["endpoint"] == "product_revenue":
    url = f"http://127.0.0.1:8000/sales?product={decision['product']}"

data = requests.get(url).json()

# Explain result
explain = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": "Explain clearly for business user"},
        {"role": "user", "content": str(data)}
    ]
)

print("\nAnswer:")
print(explain.choices[0].message.content)
