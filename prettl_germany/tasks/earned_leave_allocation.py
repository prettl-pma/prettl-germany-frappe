import frappe
from datetime import datetime, date

def allocate_earned_leave():
    today = date.today()

    next_year = today.year + 1
    leave_type = "Earned Leave"

    # Allowed companies
    allowed_companies = [
        "Prebo Automotive Private Limited",
        "Prettl mechatronics & Actuators Services Private Limited"
    ]

    # Get all active employees
    employees = frappe.get_all(
        "Employee",
        filters={
            "status": "Active",
            "company": ["in", allowed_companies]
        },
        fields=["name", "date_of_joining", "company"]
    )

    for emp in employees:
        doj = emp.date_of_joining

        # Calculate earned leaves
        if doj.year < today.year:  
            # Joined before this year → full 18 leaves
            leave_count = 18
        else:
            # Joined this year → pro rata for next year
            months_worked = 12 - doj.month + 1
            leave_count = round((18 / 12) * months_worked * 2) / 2  # round to 0.5

        # Skip if 0 leaves (HRMS validation)
        if leave_count == 0:
            continue

        # Prevent duplicate allocation for next year
        exists = frappe.db.exists(
            "Leave Allocation",
            {
                "employee": emp.name,
                "leave_type": leave_type,
                "from_date": f"{today.year}-12-26",
                "to_date": f"{next_year}-12-25",
                "docstatus": 1
            }
        )

        if exists:
            continue

        # Create Leave Allocation
        allocation = frappe.get_doc({
            "doctype": "Leave Allocation",
            "employee": emp.name,
            "leave_type": leave_type,
            "from_date": f"{today.year}-12-26",
            "to_date": f"{next_year}-12-25",
            "new_leaves_allocated": leave_count,
            "company": emp.company,
        })

        allocation.insert(ignore_permissions=True)
        allocation.submit()