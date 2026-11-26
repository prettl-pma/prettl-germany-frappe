
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

    # Period: 26th current month to 25th next month
    from_date = date(today.year, today.month, 26)

    # Calculate next month correctly
    if today.month == 12:
        to_date = date(today.year + 1, 1, 25)
    else:
        to_date = date(today.year, today.month + 1, 25)

    # Fetch active employees from allowed companies
    employees = frappe.get_all(
        "Employee",
        filters={
            "status": "Active",
            "company": ["in", allowed_companies]
        },
        fields=["name", "company", "gender", "saturday_working"]
    )

    for emp in employees:

        # Saturday Leave only if Saturday Working is enabled
        if emp.saturday_working:

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

            if not exists:
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

        # Menstrual Leave only for female employees
        if emp.gender == "Female":

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

            if not ml_exist:
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

