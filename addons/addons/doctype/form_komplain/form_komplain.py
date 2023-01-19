# -*- coding: utf-8 -*-
# Copyright (c) 2020, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class FormKomplain(Document):
	def get_data_so(self):
		for row in self.sales_order:
			list_item = frappe.db.sql(""" SELECT item_code, item_name, qty, uom, rate 
				FROM `tabSales Order Item` WHERE parent = "{}" """.format(row.nomor_so),as_dict=1)

			self.so_items = []
			for row in list_item:
				satu_item = {
					"item_code" : row.item_code,
					"item_name" : row.item_name,
					"qty" : row.qty,
					"uom" : row.uom,
					"harga" : row.rate
				}
				self.append("so_items", satu_item)
