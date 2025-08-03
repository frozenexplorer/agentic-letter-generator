from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from generator.offer_builder import generate_offer_letter
from data_loader import employee_parser
from fastapi.staticfiles import StaticFiles
import os
from http.client import HTTPException
from django.http import FileResponse

app = FastAPI()

# Serve static offers
app.mount("/files", StaticFiles(directory="./offers"), name="files")

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or use ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Load employees
employees = employee_parser.load_employee_data("./data/employees/Employee_List.csv")


@app.post("/generate-offer")
async def generate(request: Request):
    data = await request.json()
    name = data.get("name")

    emp = next(
        (e for e in employees if e["Employee Name"].lower() == name.lower()), None
    )
    if not emp:
        return {"success": False}

    paths = generate_offer_letter(emp)
    return {
        "success": True,
        "paths": {
            "pdf": os.path.basename(paths["pdf"]),
            "txt": os.path.basename(paths["txt"]),
        },
    }


OFFERS_DIR = "offers"


@app.get("/files/{filename}")
async def download_offer(filename: str):
    file_path = os.path.join(OFFERS_DIR, filename)
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    # FileResponse with `filename=` automatically sets
    # Content-Disposition: attachment; filename="…"
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/pdf",  # or "text/plain" for .txt
    )
