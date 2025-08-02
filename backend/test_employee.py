from data_loader import employee_parser

if __name__ == "__main__":
    path = "D:\\agentic letter generator\\data\\employees\\Employee_List.csv"
    employees = employee_parser.load_employee_data(path)

    print(f"✅ Loaded {len(employees)} employees")
    for emp in employees:
        print(f"- {emp['Employee Name']} ({emp['Department']}), Band: {emp['Band']}, Joining: {emp['Joining Date']}")


