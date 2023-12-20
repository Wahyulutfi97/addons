// Copyright (c) 2020, DAS and contributors
// For license information, please see license.txt

frappe.ui.form.on('Form Teknisi', {
	refresh: function(frm) {
		if(cur_frm.doc.rincian_aktualisasi_ca){
			var tot = 0
			for(var i=0;i<cur_frm.doc.rincian_aktualisasi_ca.length;i++){
				tot = tot + cur_frm.doc.rincian_aktualisasi_ca[i].total
			}
			cur_frm.set_value("grand_total_ca",tot)
		}
	}
});

cur_frm.set_query("nomor_so", "sales_order", function(doc, cdt, cdn) {
	var d = locals[cdt][cdn];
	return{
		filters: [
			['Sales Order', 'customer', '=', doc.customer]
		]
	}
});

cur_frm.set_query("penjadwalan_instalasi_dan_servis", function(doc, cdt, cdn) {
	return{
		filters: [
			['Form Teknisi', 'tipe_dokumen', '=', 'Penjadwalan Instalasi & Servis'],
			['Form Teknisi', 'docstatus', '=', '1'],	
		]
	}
});

cur_frm.set_query("spk", function(doc, cdt, cdn) {
	return{
		filters: [
			['Form Teknisi', 'tipe_dokumen', '=', 'SPK'],
			['Form Teknisi', 'docstatus', '=', '1'],	
		]
	}
});

cur_frm.set_query("form_ce", function(doc, cdt, cdn) {
	return{
		filters: [
			['Form Teknisi', 'tipe_dokumen', '=', 'Form CE'],
			['Form Teknisi', 'docstatus', '=', '1'],	
		]
	}
});

cur_frm.cscript.custom_nominal = function(doc){
	if(doc.nominal){
		doc.komisi = doc.nominal * 30 /100
		refresh_field("komisi")
	}
}

cur_frm.cscript.custom_tipe_spk = function(doc){
	if(doc.tipe_spk == "Customer" && doc.tipe_dokumen == "SPK"){
		doc.naming_series = "#####/SPK/DEPRINTZ/#MMM#/#YYYY#"
		refresh_field("naming_series")
	}
	else if(doc.tipe_spk == "Internal" && doc.tipe_dokumen == "SPK"){
		doc.naming_series = "######"
		refresh_field("naming_series")
	}
	else{
		doc.naming_series = "FT-######"
		refresh_field("naming_series")
	}
}

cur_frm.cscript.custom_validate = function(doc){
	if(doc.tipe_spk == "Customer" && doc.tipe_dokumen == "SPK"){
		doc.naming_series = "#####/SPK/DEPRINTZ/#MMM#/#YYYY#"
		// refresh_field("naming_series")
		// frappe.call({
		// 	method: "addons.addons.doctype.form_teknisi.form_teknisi.get_naming",
		// 	args: {
		// 		naming_series: doc.naming_series
		// 	},
		// 	callback: function(r) {
		// 		doc.naming = r["message"]	
		// 		refresh_field("naming")
		// 	}
		// });
	}
	else if(doc.tipe_spk == "Internal" && doc.tipe_dokumen == "SPK"){
		doc.naming_series = "######"
		// refresh_field("naming_series")
		// frappe.call({
		// 	method: "addons.addons.doctype.form_teknisi.form_teknisi.get_naming",
		// 	args: {
		// 		naming_series: doc.naming_series
		// 	},
		// 	callback: function(r) {
		// 		doc.naming = r["message"]	
		// 		refresh_field("naming")
		// 	}
		// });
	}
	else{
		doc.naming_series = "FT-######"
		// refresh_field("naming_series")
		// frappe.call({
		// 	method: "addons.addons.doctype.form_teknisi.form_teknisi.get_naming",
		// 	args: {
		// 		naming_series: doc.naming_series
		// 	},
		// 	callback: function(r) {
		// 		doc.naming = r["message"]	
		// 		refresh_field("naming")
		// 	}
		// });
	}
}

cur_frm.cscript.custom_tipe_dokumen = function(doc){
	if(doc.tipe_spk == "Customer" && doc.tipe_dokumen == "SPK"){
		doc.naming_series = "#####/SPK/DEPRINTZ/#MMM#/#YYYY#"
		refresh_field("naming_series")
	}
	else if(doc.tipe_spk == "Internal" && doc.tipe_dokumen == "SPK"){
		doc.naming_series = "######"
		refresh_field("naming_series")
	}
	else{
		doc.naming_series = "FT-######"
		refresh_field("naming_series")
	}
}

cur_frm.cscript.custom_nominal = function(doc,cdt,cdn){
	var d = locals[cdt][cdn]
	if(d.nominal && d.qty){
		d.amount = d.nominal * d.qty
		refresh_field("rincian_pengeluaran")
	}
}

cur_frm.cscript.custom_qty = function(doc,cdt,cdn){
	var d = locals[cdt][cdn]
	if(d.nominal && d.qty){
		d.amount = d.nominal * d.qty
		refresh_field("rincian_pengeluaran")
	}
}


cur_frm.cscript.custom_tipe_tiket = function(doc,cdt,cdn){
	var baris = locals[cdt][cdn]
	if(baris.tipe_tiket == "Tiket Pesawat" || baris.tipe_tiket == "Tiket Kereta" || baris.tipe_tiket == "Tiket Travel"){
		baris.satuan = "Tiket"
	}
	else{
		baris.satuan = "Hari"
	}
	refresh_field("rincian_pengeluaran")
}


cur_frm.add_fetch("item_code","item_name","item_name")

// cur_frm.cscript.custom_customer = function(doc){
// 	if(doc.customer){
// 		frappe.call({
// 			method: "addons.addons.doctype.form_teknisi.form_teknisi.get_customer_details",
// 			args: {
// 				customer: doc.customer
// 			},
// 			callback: function(r) {
// 				doc.alamat_kota =  r["message"][0][0]
// 				refresh_field("alamat_kota")
// 			}
// 		});
// 	}
// }



// cur_frm.add_fetch("penjadwalan_instalasi_dan_servis","troubleshoot","troubleshoot")
cur_frm.add_fetch("penjadwalan_instalasi_dan_servis","customer","customer")
cur_frm.add_fetch("penjadwalan_instalasi_dan_servis","item_code","item_code")
cur_frm.add_fetch("penjadwalan_instalasi_dan_servis","item_name","item_name")
cur_frm.add_fetch("penjadwalan_instalasi_dan_servis","posting_date","jadwal_instalasi_training")
// cur_frm.add_fetch("penjadwalan_instalasi_dan_servis","tanggal_penjadwalan_awal_1","tanggal_penjadwalan_awal")
cur_frm.add_fetch("penjadwalan_instalasi_dan_servis","hasil_instalasi_training","keterangan")
cur_frm.add_fetch("penjadwalan_instalasi_dan_servis","nama_teknisi","penanggung_jawab_instalasi")
cur_frm.add_fetch("spk","penanggung_jawab_instalasi","nama_teknisi_servis")
cur_frm.add_fetch("spk","customer","customer")
cur_frm.add_fetch("spk","item_code","item_code")
cur_frm.add_fetch("spk","item_name","item_name")
// cur_frm.add_fetch("spk","troubleshoot","troubleshoot")
cur_frm.add_fetch("spk","posting_date","tanggal_servis")
// cur_frm.add_fetch("spk","jenis","tindakan")