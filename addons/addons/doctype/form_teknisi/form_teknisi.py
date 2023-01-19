# -*- coding: utf-8 -*-
# Copyright (c) 2020, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from datetime import datetime

class FormTeknisi(Document):
	def autoname(self):
		naming_series = self.naming_series
		check_series = 1
		series = naming_series

		if naming_series == "######" or naming_series == "FT-######":
			check = 0
			while check == 0:
				# kalau # nya nambah ini perlu di ganti dari 3 menjadi lain
				no_series = str(check_series).zfill(6)
				# ini juga di ganti ### ke yang lain
				n = series.replace("######", no_series)

				patokan = frappe.get_all("Form Teknisi", filters={'name': n}, fields=['name'])
				if patokan:
					check_series = int(check_series) + 1
				else:
					check = 1

		elif naming_series == "#####/SPK/DEPRINTZ/#MMM#/#YYYY#":
			check = 0
			while check == 0:
				# kalau # nya nambah ini perlu di ganti dari 3 menjadi lain
				no_series = str(check_series).zfill(5)
				# ini juga di ganti ### ke yang lain
				n = series.replace("#####", no_series)
				today = datetime.today()

				n = n.replace("#YYYY#", str(today.year))
				
				rom_switcher={
	                1:'I',
	                2:'II',
	                3:'III',
	                4:'IV',
	                5:'V',
	                6:'VI',
	                7:'VII',
	                8:'VIII',
	                9:'IX',
	                10:'X',
	               	11:'XI',
	               	12:'XII'
	             }
				n = n.replace("#MMM#", str(rom_switcher.get(today.month)))
				
				patokan = frappe.get_all("Form Teknisi", filters={'name': n}, fields=['name'])
				if patokan:
					check_series = int(check_series) + 1
				else:
					check = 1
					
		self.name = n
		return n


	def get_penjadwalan(self):
		if self.penjadwalan_instalasi_dan_servis :
			get_pids = frappe.get_doc("Form Teknisi", self.penjadwalan_instalasi_dan_servis)
			
			self.tabel_nama_teknisi = get_pids.tabel_nama_teknisi
			self.jenis = get_pids.kebutuhan
			self.tanggal_penjadwalan_awal_1 = get_pids.tanggal_penjadwalan_awal
			self.tanggal_penjadwalan_akhir_1 = get_pids.tanggal_penjadwalan_akhir
			self.sales_order = get_pids.sales_order
			self.hasil_instalasi_training = get_pids.keterangan


	def get_data_spk(self):
		if self.spk :
			get_pids = frappe.get_doc("Form Teknisi", self.spk)
			
			self.tabel_nama_teknisi = get_pids.tabel_nama_teknisi
			self.sales_order = get_pids.sales_order


	def get_data_ce(self):
		if self.form_ce :
			# frappe.msgprint(self.form_ce)
			get_pids = frappe.get_doc("Form Teknisi", self.form_ce)
			self.customer = get_pids.customer
			self.customer_name = get_pids.customer_name
			self.sales_order = get_pids.sales_order
			self.tabel_nama_teknisi = get_pids.tabel_nama_teknisi
			
			self.kebutuhan_ca = get_pids.kebutuhan_ce
			self.transport_ca = get_pids.transport

			self.total_biaya = get_pids.total_biaya
			self.rincian_estimasi_ce = []
			self.deposit_teknisi = []
			self.deposit_kantor = []

			for row in get_pids.rincian_estimasi:

				self.append("rincian_estimasi", row)

			for row in get_pids.deposit_teknisi:
				self.append("deposit_teknisi",row)

			for row in get_pids.deposit_kantor:
				self.append("deposit_kantor",row)
				




	def validate(self):
		naming_series = self.naming_series
		check_series = 1
		series = naming_series

		if naming_series == "######" or naming_series == "FT-######":
			check = 0
			while check == 0:
				# kalau # nya nambah ini perlu di ganti dari 3 menjadi lain
				no_series = str(check_series).zfill(6)
				# ini juga di ganti ### ke yang lain
				n = series.replace("######", no_series)

				patokan = frappe.get_all("Form Teknisi", filters={'name': n}, fields=['name'])
				if patokan:
					check_series = int(check_series) + 1
				else:
					check = 1

		elif naming_series == "#####/SPK/DEPRINTZ/#MMM#/#YYYY#":
			check = 0
			while check == 0:
				# kalau # nya nambah ini perlu di ganti dari 3 menjadi lain
				no_series = str(check_series).zfill(5)
				# ini juga di ganti ### ke yang lain
				n = series.replace("#####", no_series)
				today = datetime.today()

				n = n.replace("#YYYY#", str(today.year))
				
				rom_switcher={
	                1:'I',
	                2:'II',
	                3:'III',
	                4:'IV',
	                5:'V',
	                6:'VI',
	                7:'VII',
	                8:'VIII',
	                9:'IX',
	                10:'X',
	               	11:'XI',
	               	12:'XII'
	             }
				n = n.replace("#MMM#", str(rom_switcher.get(today.month)))
				
				patokan = frappe.get_all("Form Teknisi", filters={'name': n}, fields=['name'])
				if patokan:
					check_series = int(check_series) + 1
				else:
					check = 1
		self.naming = n

		total_b = 0
		for row in self.rincian_estimasi:
			if row.qty and row.nominal:
				total_b = total_b + (row.qty * row.nominal)
		self.total_biaya = total_b

@frappe.whitelist()
def get_customer_details(customer):
	hasil = frappe.db.sql(""" SELECT CONCAT(tas.`address_line1`,", ", tas.`city`)
		FROM `tabDynamic Link` tdl
		JOIN `tabAddress` tas ON tas.name = tdl.`parent`
		JOIN `tabCustomer` tc ON tc.name = tdl.`link_name`

		WHERE tdl.link_name = "{}" AND tdl.parenttype = "Address" AND tdl.link_doctype = "Customer"
		LIMIT 1""".format(customer))

	return hasil

@frappe.whitelist()
def get_naming(naming_series):
	check_series = 1
	series = naming_series

	if naming_series == "######" or naming_series == "FT-######":
		check = 0
		while check == 0:
			# kalau # nya nambah ini perlu di ganti dari 3 menjadi lain
			no_series = str(check_series).zfill(6)
			# ini juga di ganti ### ke yang lain
			n = series.replace("######", no_series)

			patokan = frappe.get_all("Form Teknisi", filters={'name': n}, fields=['name'])
			if patokan:
				check_series = int(check_series) + 1
			else:
				check = 1

		return n

	elif naming_series == "#####/SPK/DEPRINTZ/#MMM#/#YYYY#":
		check = 0
		while check == 0:
			# kalau # nya nambah ini perlu di ganti dari 3 menjadi lain
			no_series = str(check_series).zfill(5)
			# ini juga di ganti ### ke yang lain
			n = series.replace("#####", no_series)
			today = datetime.today()

			n = n.replace("#YYYY#", str(today.year))
			
			rom_switcher={
                1:'I',
                2:'II',
                3:'III',
                4:'IV',
                5:'V',
                6:'VI',
                7:'VII',
                8:'VIII',
                9:'IX',
                10:'X',
               	11:'XI',
               	12:'XII'
             }
			n = n.replace("#MMM#", str(rom_switcher.get(today.month)))
			
			patokan = frappe.get_all("Form Teknisi", filters={'name': n}, fields=['name'])
			if patokan:
				check_series = int(check_series) + 1
			else:
				check = 1

		return n


@frappe.whitelist()
def get_naming_series(doc, method):
	naming_series = doc.naming_series
	check_series = 1
	series = naming_series

	if naming_series == "######" or naming_series == "FT-######":
		check = 0
		while check == 0:
			# kalau # nya nambah ini perlu di ganti dari 3 menjadi lain
			no_series = str(check_series).zfill(6)
			# ini juga di ganti ### ke yang lain
			n = series.replace("######", no_series)

			patokan = frappe.get_all("Form Teknisi", filters={'name': n}, fields=['name'])
			if patokan:
				check_series = int(check_series) + 1
			else:
				check = 1

		return n

	elif naming_series == "#####/SPK/DEPRINTZ/#MMM#/#YYYY#":
		check = 0
		while check == 0:
			# kalau # nya nambah ini perlu di ganti dari 3 menjadi lain
			no_series = str(check_series).zfill(5)
			# ini juga di ganti ### ke yang lain
			n = series.replace("#####", no_series)
			today = datetime.today()

			n = n.replace("#YYYY#", str(today.year))
			
			rom_switcher={
                1:'I',
                2:'II',
                3:'III',
                4:'IV',
                5:'V',
                6:'VI',
                7:'VII',
                8:'VIII',
                9:'IX',
                10:'X',
               	11:'XI',
               	12:'XII'
             }
			n = n.replace("#MMM#", str(rom_switcher.get(today.month)))
			
			patokan = frappe.get_all("Form Teknisi", filters={'name': n}, fields=['name'])
			if patokan:
				check_series = int(check_series) + 1
			else:
				check = 1

		return n
