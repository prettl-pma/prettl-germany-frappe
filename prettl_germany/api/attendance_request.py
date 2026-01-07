# Custom script for Attendance Request
# Add this in: Attendance Request doctype > Server Script (or in a custom app)

import frappe
from frappe import _

def on_submit(doc, method):
    """Send email to user when attendance request is submitted"""
    
    # Get employee email
    employee = frappe.get_doc("Employee", doc.employee)
    
    if not employee.user_id:
        frappe.log_error(
            message=f"No user ID found for employee {doc.employee}",
            title="Attendance Request Email Failed"
        )
        return
    
    # Prepare email content
    subject = _("Attendance Request Accepted")
    
    message = f"""
    <p>Dear {employee.employee_name},</p>
    
    <p>Your attendance request has been accepted.</p>
    
    <p><strong>Details:</strong></p>
    <ul>
        <li><strong>From Date:</strong> {frappe.format(doc.from_date, {'fieldtype': 'Date'})}</li>
        <li><strong>To Date:</strong> {frappe.format(doc.to_date, {'fieldtype': 'Date'})}</li>
        <li><strong>Reason:</strong> {doc.reason or 'N/A'}</li>
    </ul>
    
    <p>Thank you,<br>
    Prettl</p>
    """
    
    # Send email
    try:
        frappe.sendmail(
            recipients=[employee.user_id],
            subject=subject,
            message=message,
            reference_doctype="Attendance Request",
            reference_name=doc.name
        )
        
        frappe.msgprint(_("Email sent to {0}").format(employee.employee_name))
        
    except Exception as e:
        frappe.log_error(
            message=str(e),
            title="Attendance Request Email Failed"
        )
        frappe.msgprint(
            _("Failed to send email. Please check error log."),
            indicator="red"
        )