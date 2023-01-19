from __future__ import unicode_literals
from frappe import _ 

def get_data():
	return[
		{
			"label": _("CRM Document"),
			"items":[
				{
					"type": "doctype",
					"name": "Customer Care",
					"description": _("Customer Care"),
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Form Teknisi",
					"description": _("Form Teknisi"),
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Form Komplain",
					"description": _("Form Komplain"),
					"onboard": 1,
				},
			]
		},

		{
			"label": _("Query Reports"),
			"items":[
				{
					"type": "report",
					"is_query_report": True,
					"name": "Lead Customer",
					"doctype": "Lead",
					"onboard": 1,
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Alur New Customer",
					"doctype": "Customer",
					"onboard": 1,
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "FU New Customer",
					"doctype": "Customer",
					"onboard": 1,
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Flow Penjualan",
					"doctype": "Sales Order",
					"onboard": 1,
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Flow Pembelian",
					"doctype": "Purchase Order",
					"onboard": 1,
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Balance Sheet with Tax Filter",
					"doctype": "GL Entry",
					"onboard": 1,
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Gross Profit with Tax Filter",
					"doctype": "GL Entry",
					"onboard": 1,
				},

			]
		}

	]