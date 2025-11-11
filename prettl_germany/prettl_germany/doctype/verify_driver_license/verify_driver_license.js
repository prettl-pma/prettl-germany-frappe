// Copyright (c) 2025, Girman Tech and contributors
// For license information, please see license.txt

frappe.ui.form.on('Verify Driver License', {
    onload: function(frm) {
        // Only set on new form
        if (frm.is_new()) {
            if (!frm.doc.verifier_email) {
                frm.set_value('verifier_email', frappe.session.user);
            }

            // Fetch full name of current user
            frappe.db.get_value('User', frappe.session.user, 'full_name')
                .then(r => {
                    if (r && r.message && !frm.doc.verifier_name) {
                        frm.set_value('verifier_name', r.message.full_name);
                    }
                });
        }
    }
});