import frappe
from frappe.utils import nowdate

@frappe.whitelist(allow_guest=True)
def update_maintenance_status(uuid, status):
    """Update Car Maintenance record when user clicks email link."""
    doc = frappe.db.get_value("Car Maintenance", {"uuid": uuid, "docstatus": 0}, "name")
    if not doc:
        return
    maintenance = frappe.get_doc("Car Maintenance", doc)
    maintenance.status = status
    maintenance.date_of_completion = nowdate()
    maintenance.save(ignore_permissions=True)
    maintenance.submit()
    frappe.db.commit()