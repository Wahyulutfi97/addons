# Copyright (c) 2013, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns = [
		_("Purchase Order")+":Link/Purchase Order:150",
		_("Kode Supplier")+":Link/Supplier:50",
		_("Nama Supplier")+":Data:150",
		_("Tgl PO")+":Date:150",
		_("Purchase Receipt")+":Link/Purchase Receipt:150",
		_("Tgl PR")+":Date:150",
		_("Purchase Invoice")+":Link/Purchase Invoice:150",
		_("Tgl PI")+":Date:150",
		_("Payment Entry")+":Link/Payment Entry:150",
		_("Tgl PE")+":Date:150"
	]

	from_date = ""
	to_date = ""
	supplier = ""

	if filters.get("from_date"):
		from_date = """ AND tso.transaction_date >= "{}" """.format(filters.get("from_date"))
	if filters.get("to_date"):
		to_date = """ AND tso.transaction_date <= "{}" """.format(filters.get("to_date"))
	if filters.get("supplier"):
		supplier = """ AND tso.supplier = "{}" """.format(filters.get("supplier"))


	data = frappe.db.sql(""" 
		SELECT 
		tso.name, tso.supplier,tso.supplier_name, tso.`transaction_date`, 
		tdn.name, tdn.`posting_date`, 
		tsi.name, tsi.`posting_date`,
		tpe.name, tpe.`posting_date`
		FROM `tabPurchase Order` tso
		LEFT JOIN `tabPurchase Receipt Item` dni ON dni.`purchase_order` = tso.name AND dni.`docstatus` = 1
		LEFT JOIN `tabPurchase Receipt` tdn ON tdn.name = dni.`parent`  AND tdn.`docstatus` =1 
		LEFT JOIN `tabPurchase Invoice Item` sii ON sii.`purchase_order` = tso.name AND sii.`docstatus` = 1
		LEFT JOIN `tabPurchase Invoice` tsi ON tsi.name = sii.`parent`  AND tso.`docstatus` =1 
		LEFT JOIN `tabPayment Entry Reference` per ON per.`reference_name` = tsi.name AND per.`docstatus` = 1
		LEFT JOIN `tabPayment Entry` tpe ON tpe.name = per.parent 

		WHERE tso.`docstatus` = 1

		{} {} {}
		GROUP BY tso.name, tdn.name, tsi.name, tpe.name
		ORDER BY tso.`transaction_date`
	""".format(from_date,to_date,supplier))
	return columns, data
