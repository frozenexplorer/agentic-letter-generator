from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from generator.offer_builder import generate_offer_letter
from data_loader import employee_parser
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Serve static offers
app.mount("/files", StaticFiles(directory="../offers"), name="files")

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or use ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Load employees
employees = employee_parser.load_employee_data("../data/employees/Employee_List.csv")

@app.post("/generate-offer")
async def generate(request: Request):
    data = await request.json()
    name = data.get("name")

    emp = next((e for e in employees if e["Employee Name"].lower() == name.lower()), None)
    if not emp:
        return {"success": False}

    paths = generate_offer_letter(emp)
    return {
        "success": True,
        "paths": {
            "pdf": os.path.basename(paths["pdf"]),
            "txt": os.path.basename(paths["txt"])
        }
    }
