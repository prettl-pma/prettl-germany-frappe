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
	
	def on_cancel(self):
		if not self.car:
			return

		# Fetch the latest previous Car Driver record for this car
		prev_driver = frappe.db.get_all(
			"Car Driver",
			filters={
				"car": self.car,
				"docstatus": 1,  # only submitted ones
			},
			fields=["driver_email", "driver_name", "handover_date", "return_date"],
			order_by="modified desc",
			limit=1
		)

		car = frappe.get_doc("Car", self.car)

		if prev_driver:
			driver = prev_driver[0]
			car.current_driver_email = driver.driver_email
			car.current_driver_name = driver.driver_name
			car.handover_date = driver.handover_date
			car.return_date = driver.return_date
		else:
			# No previous driver found → clear fields
			car.current_driver_email = None
			car.current_driver_name = None
			car.handover_date = None
			car.return_date = None

		car.save(ignore_permissions=True)