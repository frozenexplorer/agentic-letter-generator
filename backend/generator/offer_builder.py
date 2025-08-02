from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from embedding.store import VectorStore
from typing import Dict

env = Environment(loader=FileSystemLoader("templates"))

def get_policy_sections(query_tags: Dict[str, str]) -> Dict[str, str]:
    """Fetches relevant policy sections using Chroma queries"""
    store = VectorStore()
    output = {}

    queries = {
        "leave_policy": f"Leave entitlements for Band {query_tags['band']}",
        "wfo_policy": f"Work from office policy for {query_tags['department']} team",
        "travel_policy": f"Travel policy for Band {query_tags['band']}"
    }

    for key, query in queries.items():
        results = store.similarity_search(query)
        if results["documents"][0]:
            output[key] = results["documents"][0][0][:800]  # Take top result
        else:
            output[key] = "Not found"

    return output

def generate_offer_letter(employee: Dict) -> str:
    """Fills the Jinja2 template with employee and policy data"""
    template = env.get_template("offer_template.txt")

    # Query Chroma for dynamic sections
    policy_sections = get_policy_sections({
        "band": employee["Band"],
        "department": employee["Department"]
    })

    filled = template.render(
        current_date=datetime.today().strftime("%B %d, %Y"),
        employee_name=employee["Employee Name"],
        position="Software Engineer",  # Can be dynamic later
        band=employee["Band"],
        department=employee["Department"],
        location=employee["Location"],
        joining_date=employee["Joining Date"],
        base_salary=employee["Base Salary (INR)"],
        performance_bonus=employee["Performance Bonus (INR)"],
        retention_bonus=employee["Retention Bonus (INR)"],
        total_ctc=employee["Total CTC (INR)"],
        leave_policy=policy_sections["leave_policy"],
        wfo_policy=policy_sections["wfo_policy"],
        travel_policy=policy_sections["travel_policy"]
    )

    return filled
