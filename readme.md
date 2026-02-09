# AI Data Analyst (Chat With Your CSV)

A web application that lets users upload any CSV dataset and ask questions in natural language.

The system uses an LLM to generate pandas code dynamically, executes it safely, and returns human-readable answers.

## Features
- Upload dataset
- Ask questions in plain English
- Context-aware follow-up questions
- Automatic data analysis
- Works with any CSV structure

## Tech Stack
- FastAPI
- Groq LLM (Llama 3)
- Pandas
- Python
- HTML (Jinja2 templates)

## Example Questions
- total revenue
- average price
- highest selling product
- what about apples?

## How it works
1. User uploads CSV
2. LLM generates pandas code
3. Python executes code
4. LLM explains result

This project demonstrates LLM tool-use and code interpreter architecture.

#data API service
a backend that exposes database data via API
features
upload csv
store in SQLlite/postgres
query via endpoint.