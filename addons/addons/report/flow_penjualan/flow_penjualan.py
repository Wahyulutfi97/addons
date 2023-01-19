# Copyright (c) 2013, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns = [
		_("Sales Order")+":Link/Sales Order:150",
		_("Customer")+":Link/Customer:150",
		_("Tgl SO")+":Date:150",
		_("Delivery Note")+":Link/Delivery Note:150",
		_("Tgl DN")+":Date:150",
		_("Sales Invoice")+":Link/Sales Invoice:150",
		_("Tgl SI")+":Date:150",
		_("Payment Entry")+":Link/Payment Entry:150",
		_("Tgl PE")+":Date:150"
	]

	from_date = ""
	to_date = ""
	customer = ""

	if filters.get("from_date"):
		from_date = """ AND tso.transaction_date >= "{}" """.format(filters.get("from_date"))
	if filters.get("to_date"):
		to_date = """ AND tso.transaction_date <= "{}" """.format(filters.get("to_date"))
	if filters.get("customer"):
		customer = """ AND tso.customer = "{}" """.format(filters.get("customer"))

	data = frappe.db.sql(""" 
		SELECT 
		tso.name, tso.customer, tso.`transaction_date`, 
		tdn.name, tdn.`posting_date`, 
		tsi.name, tsi.`posting_date`,
		tpe.name, tpe.`posting_date`
		FROM `tabSales Order` tso
		LEFT JOIN `tabDelivery Note Item` dni ON dni.`against_sales_order` = tso.name AND dni.`docstatus` = 1
		LEFT JOIN `tabDelivery Note` tdn ON tdn.name = dni.`parent`  AND tdn.`docstatus` =1 
		LEFT JOIN `tabSales Invoice Item` sii ON sii.`sales_order` = tso.name AND sii.`docstatus` = 1
		LEFT JOIN `tabSales Invoice` tsi ON tsi.name = sii.`parent`  AND tso.`docstatus` =1 
		LEFT JOIN `tabPayment Entry Reference` per ON per.`reference_name` = tsi.name AND per.`docstatus` = 1
		LEFT JOIN `tabPayment Entry` tpe ON tpe.name = per.parent 

		WHERE tso.`docstatus` = 1
		{} {} {}
		GROUP BY tso.name, tdn.name, tsi.name, tpe.name
		ORDER BY tso.`transaction_date`
	""".format(from_date,to_date,customer))
	return columns, data
