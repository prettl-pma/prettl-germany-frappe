import frappe
from frappe.utils import getdate

def validate_saturday_leave(doc, method):
    if doc.leave_type != "Saturday Leave":
        return

    from_date = getdate(doc.from_date)
    to_date = getdate(doc.to_date)

    current = from_date
    while current <= to_date:
        # weekday(): Monday=0 ... Saturday=5 Sunday=6
        if current.weekday() != 5:
            frappe.throw(
                "Saturday Leave can only be applied for Saturdays."
            )
        current = frappe.utils.add_days(current, 1)
