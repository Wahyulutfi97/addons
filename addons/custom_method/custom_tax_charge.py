# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
import json
from frappe.utils import cstr, flt, getdate, cint, nowdate, add_days, get_link_to_form, strip_html
from six import string_types

@frappe.whitelist()
def customTax_sales_order():
	data = frappe.db.get_list('Sales Order', filters = { 'total_taxes_and_charges': ['!=', ""] })
	for i in data :
		doc = frappe.get_doc("Sales Order", i['name'])
		doc.total_tax = 0
		doc.total_char = 0
		taxes = 0
		charges = 0
		for d in doc.get("taxes"):
			if d.charge_type == "On Net Total":
				taxes = taxes + d.base_tax_amount
			else :
				charges = charges + d.base_tax_amount
		doc.total_tax = taxes
		doc.total_char = charges
		doc.db_update()
		frappe.db.commit()

@frappe.whitelist()
def customTax_sinv():
	data = frappe.db.get_list('Sales Invoice', filters = { 'total_taxes_and_charges': ['!=', ""] })
	for i in data :
		doc = frappe.get_doc("Sales Invoice", i['name'])
		doc.total_tax = 0
		doc.total_char = 0
		taxes = 0
		charges = 0
		for d in doc.get("taxes"):
			if d.charge_type == "On Net Total":
				taxes = taxes + d.base_tax_amount
			else :
				charges = charges + d.base_tax_amount
		doc.total_tax = taxes
		doc.total_char = charges
		doc.db_update()
		frappe.db.commit()