# Copyright (c) 2026, Girman Tech and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import getdate


def execute(filters=None):
    if not filters:
        filters = {}

    columns = get_columns()
    data = get_data(filters)

    return columns, data


def get_columns():
    return [
        {
            "label": "Employee",
            "fieldname": "employee",
            "fieldtype": "Link",
            "options": "Employee",
            "width": 130,
        },
        {
            "label": "Employee Name",
            "fieldname": "employee_name",
            "fieldtype": "Data",
            "width": 180,
        },
        {
            "label": "Total Present",
            "fieldname": "total_present",
            "fieldtype": "Int",
            "width": 120,
        },
        {
            "label": "Total Absent",
            "fieldname": "total_absent",
            "fieldtype": "Int",
            "width": 120,
        },
        {
            "label": "Total Half Day",
            "fieldname": "total_half_day",
            "fieldtype": "Int",
            "width": 120,
        },
        {
            "label": "Total Leave Taken",
            "fieldname": "total_leave",
            "fieldtype": "Float",
            "width": 150,
        },
        {
            "label": "Total Holiday",
            "fieldname": "total_holiday",
            "fieldtype": "Int",
            "width": 120,
        },
        {
            "label": "Total Working Hours",
            "fieldname": "total_working_hours",
            "fieldtype": "Float",
            "width": 180,
        },
    ]


def get_data(filters):
    if not filters.get("company") or not filters.get("from_date") or not filters.get("to_date"):
        frappe.throw("Please select Company, From Date and To Date")

    from_date = getdate(filters.get("from_date"))
    to_date = getdate(filters.get("to_date"))

    employees = frappe.get_all(
        "Employee",
        filters={"company": filters.get("company"), "status": "Active"},
        fields=["name", "employee_name", "holiday_list"],
    )

    data = []

    # Get company default holiday list once
    company_default_holiday = frappe.db.get_value(
        "Company", filters.get("company"), "default_holiday_list"
    )

    for emp in employees:

        # Holiday List fallback logic
        holiday_list = emp.holiday_list or company_default_holiday

        # Count Holidays
        holiday_count = 0
        if holiday_list:
            holiday_count = frappe.db.count(
                "Holiday",
                {
                    "parent": holiday_list,
                    "holiday_date": ["between", [from_date, to_date]],
                },
            )

        # Fetch Attendance
        attendance_records = frappe.get_all(
            "Attendance",
            filters={
                "employee": emp.name,
                "attendance_date": ["between", [from_date, to_date]],
                "docstatus": 1,
            },
            fields=["status", "working_hours"],
        )

        total_present = 0
        total_absent = 0
        total_half_day = 0
        total_leave = 0
        total_working_hours = 0

        for att in attendance_records:
            if att.status == "Present":
                total_present += 1
            elif att.status == "Absent":
                total_absent += 1
            elif att.status == "Half Day":
                total_half_day += 1
            elif att.status == "On Leave":
                total_leave += 1

            total_working_hours += att.working_hours or 0

        data.append(
            {
                "employee": emp.name,
                "employee_name": emp.employee_name,
                "total_present": total_present,
                "total_absent": total_absent,
                "total_half_day": total_half_day,
                "total_holiday": holiday_count,
                "total_leave": total_leave,
                "total_working_hours": total_working_hours,
            }
        )

    return data
