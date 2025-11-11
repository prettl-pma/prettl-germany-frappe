# Copyright (c) 2025, Girman Tech and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class VerifyDriverLicense(Document):
	def on_submit(self):
		driver_license_doc = frappe.get_doc("Driver License", self.driver_email)
		driver_license_doc.append("driver_license_verifier_details",{
			"verifier_name": self.verifier_name,
			"verification_date": self.verification_date,
			"status": self.status
		})
		driver_license_doc.save(ignore_permissions=True)