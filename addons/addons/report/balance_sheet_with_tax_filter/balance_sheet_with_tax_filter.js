
// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.require("assets/erpnext/js/financial_statements.js", function() {
	frappe.query_reports["Balance Sheet with Tax Filter"] = $.extend({}, erpnext.financial_statements);


	frappe.query_reports["Balance Sheet with Tax Filter"]["filters"].push({
		"fieldname": "jenis_transaksi",
		"label": __("Tax Status"),
		"fieldtype": "Select",
		"options": 'Non PPN\nPPN',
		"default": "Non PPN"
	});


	frappe.query_reports["Balance Sheet with Tax Filter"]["filters"].push({
		"fieldname": "accumulated_values",
		"label": __("Accumulated Values"),
		"fieldtype": "Check",
		"default": 1
	});

	frappe.query_reports["Balance Sheet with Tax Filter"]["filters"].push({
		"fieldname": "include_default_book_entries",
		"label": __("Include Default Book Entries"),
		"fieldtype": "Check",
		"default": 1
	});
});
