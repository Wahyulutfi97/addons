// frappe.ui.form.on('Purchase Receipt', {
// 	onload: function(frm){
// 	    if (frm.doc.jenis_transaksi == "PPN"){
// 	        frm.set_value("taxes_and_charges","PPN 11% - D");
// 	        frm.set_value("tax_status","Tax")
// 	        frm.set_value("naming_series","ACC-PAY-P-.YY.-.MM.-.#####");

// 	    } else if (frm.doc.jenis_transaksi == "Non PPN"){
// 	    	for (var i = frm.doc.taxes.length - 1; i >= 0; i--) {
// 	    		frappe.model.set_value(cur_frm.doc.taxes[i].doctype,cur_frm.doc.taxes[i].name,"rate",0)
// 	    	}
// 	        frm.set_value("taxes_and_charges",null);
// 	        frm.set_value("taxes",null);
// 	        frm.refresh_field("taxes");

// 	        frm.set_value("tax_status","Non Tax")
// 	        frm.set_value("naming_series","ACC-PAY-NP-.YY.-.MM.-.#####");
// 	    }
// 	},
// 	jenis_transaksi: function(frm){
// 	    if (frm.doc.jenis_transaksi == "PPN"){
// 	        frm.set_value("taxes_and_charges","PPN 11% - D");
// 	        frm.set_value("tax_status","Tax")
// 	        frm.set_value("naming_series","ACC-PAY-P-.YY.-.MM.-.#####");

// 	    } else if (frm.doc.jenis_transaksi == "Non PPN"){
// 	    	for (var i = frm.doc.taxes.length - 1; i >= 0; i--) {
// 	    		frappe.model.set_value(cur_frm.doc.taxes[i].doctype,cur_frm.doc.taxes[i].name,"rate",0)
// 	    	}
// 	        frm.set_value("taxes_and_charges",null);
// 	        frm.set_value("taxes",null);
// 	        frm.refresh_field("taxes");

// 	        frm.set_value("tax_status","Non Tax")
// 	        frm.set_value("naming_series","ACC-PAY-NP-.YY.-.MM.-.#####");
// 	    }
// 	}
// })
