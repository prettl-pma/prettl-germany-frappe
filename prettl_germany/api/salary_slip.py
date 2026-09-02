# Helpers for the Salary Slip print format.
# Only the companies in HEADER_COMPANIES print a payslip header. The name comes
# from that mapping; the address and logo are read from the Company record.

import frappe
from frappe.utils.caching import request_cache

from erpnext.setup.doctype.company.company import get_default_company_address

# Address parts printed on the payslip, in order, before the pincode
ADDRESS_FIELDS = ("address_line1", "address_line2", "city", "state")

# Box the logo has to fit into, in px
LOGO_MAX_WIDTH = 195
LOGO_MAX_HEIGHT = 70

# Companies whose payslips carry a header, mapped to the name to print on it
# (PMA trades under a different name than its Company record). Any company not
# listed here prints its payslip without a header.
HEADER_COMPANIES = {
    "Prebo Automotive Private Limited": "Prebo Automotive Private Limited",
    "Prettl mechatronics & Actuators Services Private Limited": (
        "PMA Production & Services Private Limited"
    ),
}


@request_cache
def get_company_header(company):
    """Return the company name, single line address and logo for the payslip header.

    Cached per request so printing a whole payroll run looks up each company once.
    """

    header = frappe._dict(
        show=False, company_name="", address="", logo="", logo_width=None, logo_height=None
    )

    if not company:
        return header

    if company not in HEADER_COMPANIES:
        return header

    details = frappe.db.get_value(
        "Company", company, ["company_name", "company_logo"], as_dict=True
    )

    if not details:
        return header

    header.show = True

    header.company_name = HEADER_COMPANIES[company] or details.company_name or company
    header.logo = details.company_logo or ""
    header.address = get_company_address_line(company)
    header.logo_width, header.logo_height = get_logo_size(header.logo)

    return header


def get_logo_size(file_url):
    """Fit the logo into the header box, keeping its aspect ratio.

    wkhtmltopdf scales an image to max-width and then clamps it to max-height
    without re-deriving the width, which squashes anything taller than roughly
    3:1. Sizing it here and printing explicit width/height sidesteps that.
    """

    if not file_url:
        return None, None

    try:
        from PIL import Image

        file_doc = frappe.get_doc("File", {"file_url": file_url})
        with Image.open(file_doc.get_full_path()) as image:
            width, height = image.size
    except Exception:
        # unreadable or vector logo - fall back to the CSS caps
        return None, None

    if not width or not height:
        return None, None

    scale = min(LOGO_MAX_WIDTH / width, LOGO_MAX_HEIGHT / height, 1)

    return round(width * scale), round(height * scale)


def get_company_address_line(company):
    """Flatten the company's primary address into the single line the payslip prints."""

    address_name = get_default_company_address(company)

    if not address_name:
        return ""

    address = frappe.db.get_value(
        "Address", address_name, [*ADDRESS_FIELDS, "pincode"], as_dict=True
    )

    if not address:
        return ""

    line = ", ".join(address.get(field) for field in ADDRESS_FIELDS if address.get(field))

    if address.pincode:
        line = f"{line} - {address.pincode}" if line else address.pincode

    return line
