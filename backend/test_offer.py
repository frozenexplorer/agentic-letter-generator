import os
from data_loader import employee_parser
from generator import offer_builder

if __name__ == "__main__":
    employees = employee_parser.load_employee_data("../data/employees/Employee_List.csv")
    os.makedirs("../offers", exist_ok=True)

    for emp in employees:
        offer = offer_builder.generate_offer_letter(emp)
        filename = emp['Employee Name'].replace(" ", "_") + "_offer.txt"
        with open(f"../offers/{filename}", "w", encoding="utf-8") as f:
            f.write(offer)
        print(f"✅ Offer saved for {emp['Employee Name']}")

