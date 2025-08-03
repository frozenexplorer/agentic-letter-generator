from data_loader import employee_parser
from generator.offer_builder import generate_offer_letter

if __name__ == "__main__":
    path = "../data/employees/Employee_List.csv"
    employees = employee_parser.load_employee_data(path)

    for emp in employees:
        paths = generate_offer_letter(emp)
        print(f"✅ TXT: {paths['txt']}")
        print(f"✅ PDF: {paths['pdf']}")
        break  # just test with one employee
