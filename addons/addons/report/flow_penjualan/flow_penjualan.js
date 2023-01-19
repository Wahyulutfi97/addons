// Copyright (c) 2016, DAS and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Flow Penjualan"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("Sales Order From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 1
		},
		{
			"fieldname":"to_date",
			"label": __("Sales Order To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},
		{
			"fieldname":"customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer"
		},
	]
};
