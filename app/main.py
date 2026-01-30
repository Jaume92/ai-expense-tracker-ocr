from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image
import os
import uuid

from app.db.database import init_db, insert_expense, get_expenses
from app.ocr.ocr_service import extract_text
from app.parser.receipt_parser import parse_receipt


app = FastAPI(title="AI Expense Tracker")

# ---------- INIT DATABASE ----------
init_db()

# ---------- PATHS ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "..", "uploads")
FRONTEND_FOLDER = os.path.join(BASE_DIR, "frontend")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------- STATIC FILES ----------
app.mount("/uploads", StaticFiles(directory=UPLOAD_FOLDER), name="uploads")
app.mount("/dashboard", StaticFiles(directory=FRONTEND_FOLDER, html=True), name="dashboard")


# ---------- HEALTH ----------
@app.get("/")
def health():
    return {"status": "API running"}


# ---------- UPLOAD RECEIPT ----------
@app.post("/upload")
async def upload_receipt(file: UploadFile = File(...)):

    extension = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{extension}"

    file_path = os.path.join(UPLOAD_FOLDER, filename)

    # Save file
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Normalize image
    try:
        img = Image.open(file_path).convert("RGB")
        img.save(file_path, "JPEG")
    except Exception as e:
        os.remove(file_path)
        return JSONResponse(
            status_code=400,
            content={"error": f"Invalid image: {str(e)}"}
        )

    # OCR
    try:
        extracted_text = extract_text(file_path)
    except Exception as e:
        print("OCR ERROR:", e)

        return {
            "file": filename,
            "merchant": None,
            "date": None,
            "total": None
        }

    # Parser
    try:
        parsed_data = parse_receipt(extracted_text)
    except Exception as e:
        print("PARSER ERROR:", e)

        parsed_data = {
            "merchant": None,
            "date": None,
            "total": None
        }

    # Save to DB
    insert_expense(
        merchant=parsed_data.get("merchant"),
        date=parsed_data.get("date"),
        total=parsed_data.get("total"),
        file=filename
    )

    # Response clean
    return {
        "file": filename,
        "merchant": parsed_data.get("merchant"),
        "date": parsed_data.get("date"),
        "total": parsed_data.get("total")
    }


# ---------- LIST EXPENSES ----------
@app.get("/expenses")
def list_expenses():
    return get_expenses()
