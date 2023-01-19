# Copyright (c) 2013, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns = [
		_("Tanggal")+":Date:100",
		_("Nama")+":Data:200",
		_("Kota")+":Data:100",
		_("Alamat 1")+":Data:100",
		_("Alamat 2")+":Data:100",

		_("No. HP 1")+":Data:100",
		_("Email")+":Data:100",
		_("Barang")+":Data:100",
		_("Tgl FU 1")+":Date:100",
		_("Status FU 1")+":Data:100",

		_("Tgl FU 2")+":Date:100",
		_("Status FU 2")+":Data:100",
		_("Tgl FU 3")+":Date:100",
		_("Status FU 3")+":Data:100",
		_("Tgl FU 4")+":Date:100",

		_("Status FU 4")+":Data:100",
		_("Tgl FU 5")+":Date:100",
		_("Status FU 5")+":Data:100",
		_("Penerimaan")+":Data:100",
		_("Kondisi")+":Data:100",
		_("Service")+":Data:100",
		_("Respon")+":Data:100",
		_("Rekomendasi Deprintz")+":Data:100",
		_("Status FU")+":Data:100",
		_("Alasan")+":Data:120",
		_("Resume Hasil Follow Up")+":Data:200",

	]

	data = frappe.db.sql(""" SELECT 
		tcc.`tanggal`, 
		tcc.`customer`, 
		tcc.`kota`, 
		tas.`address_line1`, 
		tas.`address_line2`,

		tc.`mobile_no`, 
		tc.`email_id`,
		tcc.`item_name`,
		IFNULL(fucc.`tanggal`,"-"),
		IFNULL(fucc.`status_fu`,"-"),

		IFNULL(fucc2.`tanggal`,"-"),
		IFNULL(fucc2.`status_fu`,"-"),
		IFNULL(fucc3.`tanggal`,"-"),
		IFNULL(fucc3.`status_fu`,"-"),
		IFNULL(fucc4.`tanggal`,"-"),
		
		IFNULL(fucc4.`status_fu`,"-"),
		IFNULL(fucc5.`tanggal`,"-"),
		IFNULL(fucc5.`status_fu`,"-"),
		IFNULL(tcc.`penerimaan`,"-"),
		IFNULL(tcc.`kondisi`,"-"),
		IFNULL(tcc.`service`,"-"),
		IFNULL(tcc.`respon`,"-"),
		IFNULL(tcc.`rekomendasi_deprintz`,"-"),
		IFNULL(tcc.`status_fu`,"-"),
		IFNULL(tcc.`alasan`,"-")

		FROM `tabCustomer Care` tcc 
		JOIN `tabCustomer` tc ON tc.name = tcc.`customer`

		LEFT JOIN `tabDynamic Link` tdl ON tc.name = tdl.`link_name` AND  tdl.parenttype = "Address" AND tdl.link_doctype = "Customer"
		LEFT JOIN `tabAddress` tas ON tas.name = tdl.`parent`

		LEFT JOIN `tabFollow Up Customer Care` fucc ON fucc.parent = tcc.name AND fucc.`idx` = 1
		LEFT JOIN `tabFollow Up Customer Care` fucc2 ON fucc2.parent = tcc.name AND fucc2.`idx` = 2
		LEFT JOIN `tabFollow Up Customer Care` fucc3 ON fucc3.parent = tcc.name AND fucc3.`idx` = 3
		LEFT JOIN `tabFollow Up Customer Care` fucc4 ON fucc4.parent = tcc.name AND fucc4.`idx` = 4
		LEFT JOIN `tabFollow Up Customer Care` fucc5 ON fucc5.parent = tcc.name AND fucc5.`idx` = 5

		WHERE tcc.pilihan_customer = "Customer Baru" """)
	return columns, data
