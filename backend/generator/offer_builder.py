from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from embedding.store import VectorStore
from typing import Dict
import os, sys
import pdfkit
import shutil

if sys.platform.startswith("win"):
    wkhtmltopdf_path = r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
else:
    wkhtmltopdf_path = shutil.which("wkhtmltopdf")


env = Environment(loader=FileSystemLoader("templates"))
print("Path of wkhtmltopdf", wkhtmltopdf_path)


def get_policy_sections(query_tags: Dict[str, str]) -> Dict[str, str]:
    store = VectorStore()
    output = {}

    queries = {
        "leave_policy": f"Leave entitlements for Band {query_tags['band']}",
        "wfo_policy": f"Work from office policy for {query_tags['department']} team",
        "travel_policy": f"Travel policy for Band {query_tags['band']}",
    }

    for key, query in queries.items():
        print(f"\n🔍 Fetching: {key}")
        results = store.similarity_search(query)

        if results["documents"] and results["documents"][0]:
            best_match = results["documents"][0][0][:800]
            print(f"✅ Match found: {best_match[:100]}...")
            output[key] = best_match
        else:
            print(f"⚠️ No match for: {query}")
            output[key] = f"(⚠️ No policy match found for {key})"

    return output


def add_newlines(text: str) -> str:
    """Ensure bullet points and dashes are on new lines"""
    return text.replace("●", "\n●").replace("•", "\n•").replace("- ", "\n- ").strip()


def generate_offer_letter(employee: Dict) -> Dict[str, str]:
    """Generates both .txt and .pdf offer letters. Returns paths."""

    policy_sections = get_policy_sections(
        {"band": employee["Band"], "department": employee["Department"]}
    )

    # Add line breaks for clean formatting
    policy_sections = {k: add_newlines(v) for k, v in policy_sections.items()}

    data = {
        "current_date": datetime.today().strftime("%B %d, %Y"),
        "employee_name": employee["Employee Name"],
        "position": "Software Engineer",
        "band": employee["Band"],
        "department": employee["Department"],
        "location": employee["Location"],
        "joining_date": employee["Joining Date"],
        "base_salary": employee["Base Salary (INR)"],
        "performance_bonus": employee["Performance Bonus (INR)"],
        "retention_bonus": employee["Retention Bonus (INR)"],
        "total_ctc": employee["Total CTC (INR)"],
        "leave_policy": policy_sections["leave_policy"],
        "wfo_policy": policy_sections["wfo_policy"],
        "travel_policy": policy_sections["travel_policy"],
    }

    name_slug = employee["Employee Name"].replace(" ", "_")
    output_dir = "./offers"
    os.makedirs(output_dir, exist_ok=True)

    # 🔹 Text File
    text_template = env.get_template("offer_template.txt")
    text_content = text_template.render(data)
    txt_path = os.path.join(output_dir, f"{name_slug}_offer.txt")

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text_content)
    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

    # 🔹 PDF File
    pdf_template = env.get_template("offer_template.html")
    html = pdf_template.render(data)
    pdf_path = os.path.join(output_dir, f"{name_slug}_offer.pdf")
    pdfkit.from_string(html, pdf_path, configuration=config)

    return {"txt": txt_path, "pdf": pdf_path}
