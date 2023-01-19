from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils.background_jobs import enqueue
from frappe.model.mapper import get_mapped_doc
from frappe.model.naming import make_autoname


import json
import frappe.utils
from frappe.utils import cstr, flt, getdate, cint, nowdate, add_days, get_link_to_form
from six import string_types
from frappe.model.utils import get_fetch_values
from erpnext.stock.stock_balance import update_bin_qty, get_reserved_qty
from frappe.desk.notifications import clear_doctype_notifications
from frappe.contacts.doctype.address.address import get_company_address
from erpnext.controllers.selling_controller import SellingController
from frappe.automation.doctype.auto_repeat.auto_repeat import get_next_schedule_date
from erpnext.selling.doctype.customer.customer import check_credit_limit
from erpnext.selling.doctype.sales_order.sales_order import SalesOrder
from erpnext.stock.doctype.item.item import get_item_defaults
from erpnext.setup.doctype.item_group.item_group import get_item_group_defaults
from erpnext.manufacturing.doctype.production_plan.production_plan import get_items_for_material_requests
from erpnext.accounts.doctype.sales_invoice.sales_invoice import validate_inter_company_party, update_linked_doc,\
	unlink_inter_company_doc

from frappe.model.rename_doc import rename_doc

@frappe.whitelist()
def auto_employee_number(doc,method):
	query = frappe.db.sql(""" SELECT CONCAT("HR-EMP-",LPAD(COUNT(employee_number)+1,5,0)) AS latest FROM `tabEmployee` """)
	doc.employee_number = query[0][0]

@frappe.whitelist()
def replace_supplier_name(doc,method):
	if doc.catatan_po:
		doc.catatan_po = doc.catatan_po.replace("{{doc.supplier_name}}",doc.supplier_name)


@frappe.whitelist()
def check_biaya_order(doc,method):	
	if doc.jenis_transaksi == "Non PPN":
		doc.taxes = []
		doc.taxes_and_charges = ""
		doc.calculate_taxes_and_totals()
		doc.total_taxes = 0

	for row in doc.biaya_order_item:
		code = 0
		for row_tax in doc.taxes:
			if row_tax.item_name == row.item:
				code = 1

		if code == 0:
			if row.item and row.biaya:
				item_doc = frappe.get_doc("Item", row.item)
				account = ""
				if item_doc.biaya_account:
					account = item_doc.biaya_account
				else:
					frappe.msgprint("Nilai Field Biaya Account di Item {} - {} masih kosong, jadi tidak akan masuk ke Taxes and Charges, bisa dicek kembali.".format(row.item,row.item_name))

				if account:
					baris_tax_baru = doc.append('taxes', {})
					baris_tax_baru.charge_type = "Actual"
					baris_tax_baru.account_head = account
					baris_tax_baru.item_name = row.item
					baris_tax_baru.tax_amount = row.biaya
					baris_tax_baru.description = "Biaya Item"

					doc.run_method("calculate_taxes_and_totals")


@frappe.whitelist()
def rename_employee():
	list_employee = frappe.db.sql(""" SELECT name, employee_name 
		FROM `tabEmployee` WHERE employee_name != name """)
	for row in list_employee:
		doc_employee = frappe.get_doc("Employee", row[0])
		rename_doc("User", row[0], row[1])


@frappe.whitelist()
def rename_user():
	frappe.rename_doc("User", "ksales.deprintz@gmail.com", "purchasing7.deprintz@gmail.com")


@frappe.whitelist()
def check_enabled_sales_person(doc,method):
	if not doc.enabled:
		customer_list = frappe.db.sql(""" SELECT name FROM `tabCustomer` WHERE sales = "{}" """.format(doc.name))
		for row in customer_list:
			customer_doc = frappe.get_doc("Customer",row[0])
			if customer_doc.sales:
				customer_doc.old_sales_person = customer_doc.sales
				customer_doc.sales = ""
				customer_doc.db_update()

# email ke user jika pinv due date 2 hari lagi
@frappe.whitelist()
def auto_email_pinv_due_date():
	# ambil list PINV
	get_pinv = frappe.db.sql("""

		SELECT pinv.`name`, pinv.`due_date`, DATEDIFF(pinv.`due_date`, CURDATE()) FROM `tabPurchase Invoice` pinv
		WHERE pinv.`docstatus` = 1
		AND DATEDIFF(pinv.`due_date`, CURDATE()) = 2

	""")

	list_pinv_email = ""
	if get_pinv :
		for i in get_pinv :
			list_pinv_email = list_pinv_email + str(i[0]) + str(", ")

		subject_email = "PINV mendekati Due Date"
		body_email = "PINV berikut ini akan Due Date dalam 2 Hari\n\n" + str(list_pinv_email)
		purpose = "PINV mendekati Due Date"

		orang_diemail = ["adm01.shirly.deprintz@gmail.com","adm01.deprintz@gmail.com","purchasing.deprintz@gmail.com","purchasing.ijis.deprintz@gmail.com","finance.deprintz@gmail.com"]

		for email in orang_diemail :
			new_docu = frappe.new_doc("Document buat Notification Email")
			new_doc.purpose = purpose
			new_doc.subject_email = subject_email
			new_doc.body_email = body_email
			new_doc.recipients = email
			new_doc.flags.ignore_permission = True
			new_doc.save()

@frappe.whitelist()
def validate_so_naming(doc,method):

	if doc.jenis_transaksi == "PPN":
		doc.tax_status = "Tax"
		if doc.is_new():
			doc.naming_series = "SO-P-.YY.MM.DD.-.#####"
	else:
		doc.tax_status = "Non Tax"
		if doc.is_new():
			doc.naming_series = "SO-NP-.YY.MM.DD.-.#####"

@frappe.whitelist()
def delete_item():
	item_list = frappe.db.sql(""" SELECT name FROM `tabItem` """)
	for row in item_list:
		item = frappe.get_doc("Item", row[0])
		item.delete()
		print("Item {} is deleted".format(row[0]))
		frappe.db.commit()

@frappe.whitelist()
def autoname_customer_and_serial(doc,method):
	doc.name = doc.get_customer_name()
	doc.serial_customer = make_autoname("CUST-.YY.MM.DD.-.#####")

@frappe.whitelist()
def autoname_lead(doc,method):
	doc.yy = str(doc.posting_date).split("-")[0][-2:]
	doc.mm = str(doc.posting_date).split("-")[1]
	doc.dd = str(doc.posting_date).split("-")[2]
	doc.name = make_autoname(doc.naming_series.replace(".YY.",doc.yy).replace(".DD.",doc.dd).replace("MM",doc.mm))

@frappe.whitelist()
def test_autoname_lead():
	doc =  frappe.get_doc("Lead", "LEAD-201214-023")
	doc.yy = str(doc.posting_date).split("-")[0][-2:]
	doc.mm = str(doc.posting_date).split("-")[1]
	doc.dd = str(doc.posting_date).split("-")[2]
	frappe.throw(doc.naming_series.replace(".YY.",doc.yy).replace(".DD.",doc.dd).replace("MM",doc.mm))
	

@frappe.whitelist()
def make_delivery_note_2(source_name, target_doc=None, skip_item_mapping=False):
	def set_missing_values(source, target):
		target.ignore_pricing_rule = 1
		target.run_method("set_missing_values")
		target.run_method("set_po_nos")
		target.run_method("calculate_taxes_and_totals")

		if source.company_address:
			target.update({'company_address': source.company_address})
		else:
			# set company address
			target.update(get_company_address(target.company))

		if target.company_address:
			target.update(get_fetch_values("Delivery Note", 'company_address', target.company_address))

	def update_item(source, target, source_parent):
		target.base_amount = (flt(source.qty) - flt(source.delivered_qty)) * flt(source.base_rate)
		target.amount = (flt(source.qty) - flt(source.delivered_qty)) * flt(source.rate)
		target.qty = flt(source.qty) - flt(source.delivered_qty)

		item = get_item_defaults(target.item_code, source_parent.company)
		item_group = get_item_group_defaults(target.item_code, source_parent.company)

		if item:
			target.cost_center = frappe.db.get_value("Project", source_parent.project, "cost_center") \
				or item.get("buying_cost_center") \
				or item_group.get("buying_cost_center")

	mapper = {
		"Sales Order": {
			"doctype": "Delivery Note",
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		"Sales Taxes and Charges": {
			"doctype": "Sales Taxes and Charges",
			"add_if_empty": True
		},
		"Sales Team": {
			"doctype": "Sales Team",
			"add_if_empty": True
		},
		"Biaya Order Item": {
			"doctype": "DN Biaya Order Item",
			"add_if_empty": True
		}
	}

	if not skip_item_mapping:
		mapper["Sales Order Item"] = {
			"doctype": "Delivery Note Item",
			"field_map": {
				"rate": "rate",
				"name": "so_detail",
				"parent": "against_sales_order",
			},
			"postprocess": update_item,
			"condition": lambda doc: abs(doc.delivered_qty) < abs(doc.qty) and doc.delivered_by_supplier!=1
		}

	target_doc = get_mapped_doc("Sales Order", source_name, mapper, target_doc, set_missing_values)

	return target_doc

@frappe.whitelist()
def get_nama_teknisi(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""
        select name,employee_name,designation
		from `tabEmployee`
		where employee_name like '%{0}%' or name like '%{0}%' or designation like '%{0}%'
		limit {1}, {2}
    """.format(txt, start, page_len))

@frappe.whitelist()
def repair_gl_entry(doctype,docname):
	
	docu = frappe.get_doc(doctype, docname)	
	delete_sl = frappe.db.sql(""" DELETE FROM `tabStock Ledger Entry` WHERE voucher_no = "{}" """.format(docname))
	delete_gl = frappe.db.sql(""" DELETE FROM `tabGL Entry` WHERE voucher_no = "{}" """.format(docname))

	frappe.db.sql(""" UPDATE `tabSingles` SET VALUE = 1 WHERE `field` = "allow_negative_stock" """)
	docu.update_stock_ledger()
	docu.make_gl_entries()
	frappe.db.sql(""" UPDATE `tabSingles` SET VALUE = 0 WHERE `field` = "allow_negative_stock" """)