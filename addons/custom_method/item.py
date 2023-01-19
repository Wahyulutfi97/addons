from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils.background_jobs import enqueue
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def delete_item():
	# item_list = frappe.db.sql(""" SELECT name FROM `tabItem` """)
	# for row in item_list:
	# 	item = frappe.get_doc("Item", row[0])
	# 	item.delete()
	# 	print("Item {} is deleted".format(row[0]))
	# 	frappe.db.commit()
	pass