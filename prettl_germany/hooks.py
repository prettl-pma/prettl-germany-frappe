app_name = "prettl_germany"
app_title = "Prettl Germany"
app_publisher = "Girman Tech"
app_description = "Customization for Prettl Germany"
app_email = "naman.agrawal@girmantech.com"
app_license = "mit"

fixtures = [
    {
        "doctype": "Web Page"
    },
    {
        "doctype": "Role",
        "filters": [
            ["name", "in", ["Car Management Edit", "Car Management Read"]]
        ]
    },
    {
        "doctype": "Custom DocPerm",
        "filters": [
            ["role", "in", ["Car Management Edit", "Car Management Read"]]
        ]
    },
    {
        "doctype": "Web Form",
        "filters": [
            ["name", "in", ["job-application"]]
        ]
    },
    {
        "doctype": "Workspace",
        "filters": [
            ["name", "in", ["Shift & Attendance", "Payroll"]]
        ]

    }
]

scheduler_events = {
    "cron": {
        # At 06:00 on 1 April
        "0 6 1 4 *": [
            "prettl_germany.tasks.car_utils.check_summer_tyre_due"
        ],
        # At 06:00 on 1 October
        "0 6 1 10 *": [
            "prettl_germany.tasks.car_utils.check_winter_tyre_due"
        ],
        # Run every 26th dec at 6:00 AM
        "0 6 26 12 *": [
            "prettl_germany.tasks.earned_leave_allocation.allocate_earned_leave"
        ],
        # Saturday Leave on 26th of every month at 3 PM
"0 15 26 * *": [
    "prettl_germany.tasks.saturday_menstural_leave_allocation.allocate_saturday_menstural_leave"
],
    }
}

doc_events = {
    "Leave Application": {
        "validate": "prettl_germany.api.leave_application.validate_saturday_leave"
    },
    "Attendance Request": {
        "on_submit": "prettl_germany.api.attendance_request.on_submit"
    }
}

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "prettl_germany",
# 		"logo": "/assets/prettl_germany/logo.png",
# 		"title": "Prettl Germany",
# 		"route": "/prettl_germany",
# 		"has_permission": "prettl_germany.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/prettl_germany/css/prettl_germany.css"
# app_include_js = "/assets/prettl_germany/js/prettl_germany.js"

# include js, css files in header of web template
# web_include_css = "/assets/prettl_germany/css/prettl_germany.css"
# web_include_js = "/assets/prettl_germany/js/prettl_germany.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "prettl_germany/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "prettl_germany/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

jinja = {
    "methods": [
        "prettl_germany.api.salary_slip.get_company_header"
    ]
}

# Installation
# ------------

# before_install = "prettl_germany.install.before_install"
# after_install = "prettl_germany.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "prettl_germany.uninstall.before_uninstall"
# after_uninstall = "prettl_germany.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "prettl_germany.utils.before_app_install"
# after_app_install = "prettl_germany.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "prettl_germany.utils.before_app_uninstall"
# after_app_uninstall = "prettl_germany.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "prettl_germany.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"prettl_germany.tasks.all"
# 	],
# 	"daily": [
# 		"prettl_germany.tasks.daily"
# 	],
# 	"hourly": [
# 		"prettl_germany.tasks.hourly"
# 	],
# 	"weekly": [
# 		"prettl_germany.tasks.weekly"
# 	],
# 	"monthly": [
# 		"prettl_germany.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "prettl_germany.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "prettl_germany.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "prettl_germany.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["prettl_germany.utils.before_request"]
# after_request = ["prettl_germany.utils.after_request"]

# Job Events
# ----------
# before_job = ["prettl_germany.utils.before_job"]
# after_job = ["prettl_germany.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"prettl_germany.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

