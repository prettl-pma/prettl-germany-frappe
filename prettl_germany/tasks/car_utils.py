import frappe
from frappe.utils import getdate, nowdate, get_url
from datetime import date

def check_summer_tyre_due():
    """Run on 1st April at 6 AM"""
    check_tyre_due("Summer Tyre Equipment")

def check_winter_tyre_due():
    """Run on 1st October at 6 AM"""
    check_tyre_due("Winter Tyre Equipment")

def check_tyre_due(tyre_type):
    """Check all cars for missing tyre maintenance and send reminder emails."""
    today = getdate()
    year = today.year

    # Define periods based on tyre type
    if tyre_type == "Summer Tyre Equipment":
        start_date = date(year, 1, 1)
        end_date = date(year, 3, 31)
    elif tyre_type == "Winter Tyre Equipment":
        start_date = date(year, 7, 1)
        end_date = date(year, 9, 30)
    else:
        frappe.log_error(f"Unknown tyre type: {tyre_type}", "check_tyre_due")
        return

    cars = frappe.get_all("Car", fields=["name", "model", "current_driver_email", "current_driver_first_name", "current_driver_last_name"])

    for car in cars:
        exists = frappe.db.exists(
            "Car Maintenance",
            {
                "car": car.name,
                "maintenance_type": tyre_type,
                "date_of_completion": ["between", [start_date, end_date]],
                "docstatus": 1,
            },
        )

        if not exists:
            send_tyre_mail(car.name, car.model, car.current_driver_email, car.current_driver_first_name, car.current_driver_last_name, tyre_type)


def send_tyre_mail(car_name, model, driver_email, driver_first_name, driver_last_name, tyre_type):
    """Send reminder email and create draft Car Maintenance record."""

    if not driver_email:
        return

    # Create a draft Car Maintenance record
    maintenance = frappe.get_doc({
        "doctype": "Car Maintenance",
        "car": car_name,
        "maintenance_type": tyre_type,
        "docstatus": 0,
    })
    maintenance.insert(ignore_permissions=True)

    # Create action URLs
    base_url = get_url()
    complete_url = f"{base_url}/api/method/prettl_germany.api.update_maintenance.update_maintenance_status?uuid={maintenance.uuid}&status=Changed"
    not_done_url = f"{base_url}/api/method/prettl_germany.api.update_maintenance.update_maintenance_status?uuid={maintenance.uuid}&status=Unchanged"

    subject = f"{tyre_type.replace('Equipment','')} Change Due"
    message = f"""
        <p>Dear {driver_last_name}, {driver_first_name},</p>

        <p>Our records indicate that your car <b>{model} - {car_name}</b> has not had a
        <b>{tyre_type}</b> maintenance this year.</p>

        <p>Please confirm your tyre change status:</p>

        <p>
            <a href="{complete_url}" style="background-color:#28a745;color:white;padding:8px 12px;text-decoration:none;border-radius:4px;">✅ Maintenance Completed</a>
            &nbsp;&nbsp;
            <a href="{not_done_url}" style="background-color:#dc3545;color:white;padding:8px 12px;text-decoration:none;border-radius:4px;">❌ Not Completed</a>
        </p>

        <p>Thank you for your attention.</p>
        <p><b>– Prettl System</b></p>
    """

    frappe.sendmail(
        recipients=[driver_email],
        subject=subject,
        message=message,
    )