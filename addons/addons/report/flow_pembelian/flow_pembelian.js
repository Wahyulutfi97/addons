// Copyright (c) 2016, DAS and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Flow Pembelian"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("Purchase Order From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 1
		},
		{
			"fieldname":"to_date",
			"label": __("Purchase Order To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},
		{
			"fieldname":"supplier",
			"label": __("Supplier"),
			"fieldtype": "Link",
			"options": "Supplier"
		},
	]
};
