# Copyright (c) 2025, Girman Tech and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import uuid

class CarMaintenance(Document):
    def before_insert(self):
        # Generate a UUID only once
        if not self.uuid:
            self.uuid = str(uuid.uuid4())
