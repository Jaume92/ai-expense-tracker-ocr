AI Expense Tracker — OCR Invoice Processing System

AI-powered expense tracking system that automatically extracts structured data from invoice images using OCR and processes it through a FastAPI backend.

This project simulates a real-world business use case focused on automating manual expense reporting and invoice management workflows.

Features

Automatic invoice data extraction using OCR

Image upload and processing pipeline

REST API built with FastAPI

Structured invoice data output (amount, date, vendor, total)

Ready for integration with external systems

Modular and scalable backend architecture

Business Use Case

Manual expense processing is time-consuming and error-prone.

This system enables companies to:

Upload invoice images

Automatically extract relevant fields

Standardize expense data

Integrate results into accounting or BI systems

Typical applications include:

Expense management platforms

Accounting automation tools

Internal company reporting systems

SME financial dashboards

System Architecture
Client Upload
     ↓
OCR Engine
     ↓
Data Processing Layer
     ↓
FastAPI Backend
     ↓
JSON Output / Integration Layer

Tech Stack

Python

FastAPI

OCR (Tesseract / EasyOCR)

OpenCV

REST API

Installation

Clone repository:

git clone https://github.com/Jaume92/ai-expense-tracker-ocr.git
cd ai-expense-tracker-ocr


Create virtual environment:

python -m venv venv
source venv/bin/activate


Windows:

venv\Scripts\activate


Install dependencies:

pip install -r requirements.txt

Running the Application

Start backend server:

uvicorn main:app --reload


API available at:

http://127.0.0.1:8000


Swagger documentation:

http://127.0.0.1:8000/docs

Processing Workflow

Upload invoice image

OCR extracts raw text

Data processing logic parses relevant fields

Backend returns structured JSON response

Output ready for storage or integration

Planned Improvements

Support for PDF invoices

Multi-language OCR processing

Database integration

Authentication system

Frontend dashboard

Cloud deployment

Author

Developed by Jaume
Focused on applied AI systems, automation pipelines and backend integration.
