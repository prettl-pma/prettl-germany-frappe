import frappe
from datetime import date

def allocate_saturday_menstural_leave():
    today = date.today()
    leave_type = "Saturday Leave"
    menstrual_leave = "Menstrual Leave"
    # Allowed companies for allocation
    allowed_companies = [
        "Prebo Automotive Private Limited",
        "Prettl mechatronics & Actuators Services Private Limited"
    ]

    # Period: 26 current month → 25 next month
    from_date = date(today.year, today.month, 26)

    # Calculate next month correctly
    if today.month == 12:
        to_date = date(today.year + 1, 1, 25)
    else:
        to_date = date(today.year, today.month + 1, 25)

    # Fetch all active employees from ONLY allowed companies
    employees = frappe.get_all(
        "Employee",
        filters={
            "status": "Active",
            "company": ["in", allowed_companies]
        },
        fields=["name", "company", "gender"]
    )

    for emp in employees:

        # Prevent duplicate allocation
        exists = frappe.db.exists(
            "Leave Allocation",
            {
                "employee": emp.name,
                "leave_type": leave_type,
                "from_date": from_date,
                "to_date": to_date,
                "docstatus": 1
            }
        )

        if exists:
            continue

        # Create Saturday Leave Allocation
        allocation = frappe.get_doc({
            "doctype": "Leave Allocation",
            "employee": emp.name,
            "leave_type": leave_type,
            "from_date": from_date,
            "to_date": to_date,
            "new_leaves_allocated": 2,
            "company": emp.company
        })

        allocation.insert(ignore_permissions=True)
        allocation.submit()

        if emp.gender == "Female":
        # Prevent duplicate menstural leave allocation
            ml_exist = frappe.db.exists(
                "Leave Allocation",
                {
                    "employee": emp.name,
                    "leave_type": menstrual_leave,
                    "from_date": from_date,
                    "to_date": to_date,
                    "docstatus": 1
                }
            )

            if ml_exist:
                continue

            # Create Mensural Leave Allocation
            allocation = frappe.get_doc({
                "doctype": "Leave Allocation",
                "employee": emp.name,
                "leave_type": menstrual_leave,
                "from_date": from_date,
                "to_date": to_date,
                "new_leaves_allocated": 1,
                "company": emp.company
            })

            allocation.insert(ignore_permissions=True)
            allocation.submit()