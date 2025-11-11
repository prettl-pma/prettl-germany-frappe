# Copyright (c) 2025, Girman Tech and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CarDriver(Document):
	def on_submit(self):
		if self.car:
			car = frappe.get_doc("Car", self.car)
			car.current_driver_email = self.driver_email
			car.current_driver_name = self.driver_name
			car.handover_date = self.handover_date
			car.return_date = self.return_date
			car.save(ignore_permissions=True)