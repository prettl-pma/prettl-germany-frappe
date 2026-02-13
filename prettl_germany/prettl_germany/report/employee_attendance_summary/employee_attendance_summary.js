// Copyright (c) 2026, Girman Tech and contributors
// For license information, please see license.txt

frappe.query_reports["Employee Attendance Summary"] = {
    "filters": [
        {
            "fieldname": "company",
            "label": "Company",
            "fieldtype": "Link",
            "options": "Company",
            "reqd": 1
        },
        {
            "fieldname": "from_date",
            "label": "From Date",
            "fieldtype": "Date",
            "reqd": 1
        },
        {
            "fieldname": "to_date",
            "label": "To Date",
            "fieldtype": "Date",
            "reqd": 1
        }
    ]
};
