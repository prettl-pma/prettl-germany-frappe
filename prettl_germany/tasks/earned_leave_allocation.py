import frappe
from frappe.utils import now_datetime, getdate

def round_to_half(n):
    """Round a number to nearest 0.5"""
    return round(n * 2) / 2

def allocate_earned_leave():
    today = now_datetime().date()

    current_year = today.year
    fixed_leave = 18

    # Calculate last year boundaries
    last_year_start = getdate(f"{current_year - 1}-01-01")
    last_year_end = getdate(f"{current_year - 1}-12-31")

    # Fetch all active employees
    employees = frappe.get_all(
        "Employee",
        filters={"status": "Active"},
        fields=["name", "date_of_joining", "company"]
    )

    for emp in employees:
        doj = emp.date_of_joining
        if not doj:
            continue

        # CASE 1: Joined before last year → full 18 leaves
        if doj < last_year_start:
            leave_count = fixed_leave

        # CASE 2: Joined last year → pro-rata
        elif last_year_start <= doj <= last_year_end:
            # Count months worked in the last year
            months_worked = ((last_year_end.year - doj.year) * 12 +
                             (last_year_end.month - doj.month) + 1)

            leave_count = (months_worked / 12) * fixed_leave
            leave_count = round_to_half(leave_count)  # round to nearest 0.5

        # CASE 3: Joined this year → 0 leaves
        else:
            leave_count = 0

        if leave_count == 0:
            continue

        # Create Leave Allocation document
        allocation = frappe.get_doc({
            "doctype": "Leave Allocation",
            "employee": emp.name,
            "leave_type": "Earned Leave",
            "from_date": f"{current_year}-01-01",
            "to_date": f"{current_year}-12-31",
            "new_leaves_allocated": leave_count,
            "company": emp.company
        })
        print(f"Allocating {leave_count} leaves to {emp.name}")

        allocation.insert(ignore_permissions=True)
        allocation.submit()
        frappe.db.commit()
