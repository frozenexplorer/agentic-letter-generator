from data_loader import employee_parser
from generator.pdf_builder import generate_offer_pdf

if __name__ == "__main__":
    employees = employee_parser.load_employee_data("../data/employees/Employee_List.csv")
    path = generate_offer_pdf(employees[0])
    print("✅ PDF generated at:", path)
