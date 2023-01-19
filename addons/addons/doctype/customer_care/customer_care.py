# -*- coding: utf-8 -*-
# Copyright (c) 2020, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class CustomerCare(Document):
	def get_data_so(self):
		if self.sales_order_table:
			for row in self.sales_order_table:
				list_item = frappe.db.sql(""" SELECT item_code, item_name, qty, uom, rate 
					FROM `tabSales Order Item` WHERE parent = "{}" """.format(row.nomor_so),as_dict=1)

				self.item_customer_care = []
				for row in list_item:
					satu_item = {
						"item_code" : row.item_code,
						"item_name" : row.item_name,
						"qty" : row.qty,
						"uom" : row.uom,
						"harga" : row.rate
					}
					self.append("item_customer_care", satu_item)

@frappe.whitelist()
def get_customer_details(customer):
	hasil = [["-","-","-","-","-"]]
	hasil = frappe.db.sql(""" 
		SELECT tc.customer_name, tas.`city`, 
		tas.`address_line1`, tc.`mobile_no`, tc.`email_id`
		FROM `tabDynamic Link` tdl
		JOIN `tabAddress` tas ON tas.name = tdl.`parent`
		JOIN `tabCustomer` tc ON tc.name = tdl.`link_name`

		WHERE tdl.link_name = "{}" AND tdl.parenttype = "Address" AND tdl.link_doctype = "Customer"
		LIMIT 1""".format(customer))

	return hasil

@frappe.whitelist()
def get_customer_query(doctype, txt, searchfield, start, page_len, filters):
	result = frappe.db.sql("""
		select mo.name, mo.customer_name, mo.territory
		 from `tabCustomer` mo 
		where mo.name like '%{0}%' or mo.customer_name like '%{0}%'
		AND mo.disabled= 0
		order by
			mo.name
		limit {1}, {2}""".format(txt, start, page_len))

	return result

@frappe.whitelist()
def get_so_items(doctype, txt, searchfield, start, page_len, filters):
	if not filters: filters = {}

	condition = ""
	sales_order_table = []
	if filters.get("sales_order"):
		sales_order_table = filters.get("sales_order").split("|")

	# filteran = "("
	hasil_akhir = []
	for row in sales_order_table:
		if row:
			hasil = frappe.db.sql(""" SELECT ti.name, ti.description
					FROM `tabItem` ti 
					JOIN `tabSales Order Item` tso ON tso.item_code = ti.name
					WHERE tso.parent = "{}"
					""".format(row))
			if hasil:
				hasil_akhir.append(hasil[0])

	

	return hasil_akhir
