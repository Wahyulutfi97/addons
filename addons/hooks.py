# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "addons"
app_title = "Addons"
app_publisher = "DAS"
app_description = "addons"
app_icon = "octicon octicon-file-directory"
app_color = "blue"
app_email = "digitalasiasolusindo@gmail.com"
app_license = "MIT"

# fixtures = [
# 	{
# 	"dt":"Custom Field", 
# 	},
# 	{"dt":"Property Setter", 
# 	}
# 	,
# 	{"dt":"Client Script", 
# 	}
# 	,
# 	{"dt":"Print Format", 
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/addons/css/addons.css"
# app_include_js = "/assets/addons/js/addons.js"

# include js, css files in header of web template
# web_include_css = "/assets/addons/css/addons.css"
# web_include_js = "/assets/addons/js/addons.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"Customer" : "public/js/customer.js",
"Lead" : "public/js/lead.js",
"Sales Order" : "public/js/sales_order.js",
"Purchase Order" : "public/js/purchase_order.js",
"Purchase Receipt" : "public/js/purchase_receipt.js",
"Purchase Invoice" : "public/js/purchase_invoice.js",
"Delivery Note" : "public/js/delivery_note.js",
"Sales Invoice" : "public/js/sales_invoice.js",
"Quotation" : "public/js/quotation.js",
"Payment Entry" : "public/js/payment_entry.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "addons.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "addons.install.before_install"
# after_install = "addons.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "addons.notifications.get_notification_config"

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

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Customer": {
		# "autoname": "addons.custom_method_hooks.autoname_customer_and_serial"
		"autoname": "addons.custom_method.customer.autoname_customer_and_serial"
	},
	"Sales Person": {
		"validate": "addons.custom_method_hooks.check_enabled_sales_person"
	},
	"Sales Order": {
		"validate": ["addons.custom_method_hooks.check_biaya_order"],
		"before_insert" : "addons.custom_method_hooks.pinv_tax",
        # "before_update_after_submit": "rpk.doctype_function.sales_order.validate_payment_schedule_so"	
	},
	"Lead":{
		"autoname": "addons.custom_method_hooks.autoname_lead"
	},
	"Purchase Order":{
		"validate": "addons.custom_method_hooks.replace_supplier_name",
		"on_update_after_submit": "addons.custom_method_hooks.replace_supplier_name",
		"before_insert" : "addons.custom_method_hooks.pinv_tax"
	},
	"Purchase Invoice":{
		"before_insert" : "addons.custom_method_hooks.pinv_tax"
	},
	"Stock Entry":{
		"before_insert" : "addons.custom_method_hooks.pinv_tax"
	},
	"Purchase Receipt":{
		"before_insert" : "addons.custom_method_hooks.pinv_tax"
	},
	"Sales Invoice":{
		"before_insert" : "addons.custom_method_hooks.pinv_tax"
	},
	"Delivery Note":{
		"before_insert" : "addons.custom_method_hooks.pinv_tax"
	},
	
	"Employee":{
		"before_insert":"addons.custom_method_hooks.auto_employee_number"
	}

}

# Scheduled Tasks
# ---------------
scheduler_events = {
# 	"all": [
# 		"addons.tasks.all"
# 	],
	"daily": [
		"addons.custom_method_hooks.auto_email_pinv_due_date"
	],
	"hourly": [
		"addons.custom_method_hooks.isi_tax_status"
	],
# 	"weekly": [
# 		"addons.tasks.weekly"
# 	]
# 	"monthly": [
# 		"addons.tasks.monthly"
# 	]
}


# scheduler_events = {
# 	"all": [
# 		"addons.tasks.all"
# 	],
# 	"daily": [
# 		"addons.tasks.daily"
# 	],
# 	"hourly": [
# 		"addons.tasks.hourly"
# 	],
# 	"weekly": [
# 		"addons.tasks.weekly"
# 	]
# 	"monthly": [
# 		"addons.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "addons.install.before_tests"

# Overriding Methods
# ------------------------------
override_whitelisted_methods = {
 	"erpnext.accounts.doctype.payment_entry.payment_entry.get_payment_entry": "addons.custom_method.payment_entry.custom_get_payment_entry",
 	"erpnext.selling.doctype.sales_order.sales_order.make_delivery_note": "addons.custom_method.sales_order.make_delivery_note_2",
 	"erpnext.selling.doctype.sales_order.sales_order.make_sales_invoice": "addons.custom_method.sales_order.make_sales_invoice_2",
 	"erpnext.stock.doctype.delivery_note.delivery_note.make_sales_invoice": "addons.custom_method.delivery_note.make_sales_invoice_2",
 	"erpnext.buying.doctype.purchase_order.purchase_order.make_purchase_receipt": "addons.custom_method.purchase_order.make_purchase_receipt_2",
 	"erpnext.buying.doctype.purchase_order.purchase_order.make_purchase_invoice": "addons.custom_method.purchase_order.make_purchase_invoice_2",
 	"erpnext.stock.doctype.purchase_receipt.purchase_receipt.make_purchase_invoice": "addons.custom_method.purchase_receipt.make_purchase_invoice_2",
 	"erpnext.selling.doctype.sales_order.sales_order.make_purchase_order": "addons.custom_method.sales_order.make_purchase_order_2", 	
}

# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "addons.task.get_dashboard_data"
# }

