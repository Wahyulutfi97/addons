cur_frm.add_fetch("item","item_name","item_name")
frappe.ui.form.on('SI Biaya Order Item', {
	item: function(frm,cdt,cdn){
		console.log("xxx")
		if(locals[cdt][cdn].item && locals[cdt][cdn].biaya){
			frappe.call({
				method: "frappe.client.get",
				args: {
					doctype: "Item",
					name: locals[cdt][cdn].item
				},
				callback: function (data) {
					if(data){
						console.log("789")
						if(data.message["biaya_account"]){
							let item_code = locals[cdt][cdn].item
							let biaya = locals[cdt][cdn].biaya
							let account = data.message["biaya_account"]
							let check = 0
							for(var row in cur_frm.doc.taxes){
								if(cur_frm.doc.taxes[row].item_name == item_code){
									check = 1
									cur_frm.doc.taxes[row].tax_amount = biaya
								}
							}
							if(check == 0){
								console.log("456")
								var d = frappe.model.add_child(cur_frm.doc, "Sales Taxes and Charges", "taxes")
								d.charge_type = "Actual"
								d.account_head = account
								d.item_name = item_code
								d.tax_amount = biaya
								d.description = "Biaya Item"
							}
							
							cur_frm.refresh_fields("taxes")
							frm.refresh_fields()
						}
					} 
				}
			})
		}
	},
	biaya: function(frm,cdt,cdn){
		console.log("yyyy")
		if(locals[cdt][cdn].item && locals[cdt][cdn].biaya){
			frappe.call({
				method: "frappe.client.get",
				args: {
					doctype: "Item",
					name: locals[cdt][cdn].item
				},
				callback: function (data) {
					if(data){
						console.log("000")
						if(data.message["biaya_account"]){
							let item_code = locals[cdt][cdn].item
							let biaya = locals[cdt][cdn].biaya
							let account = data.message["biaya_account"]
							let check = 0
							for(var row in cur_frm.doc.taxes){
								if(cur_frm.doc.taxes[row].item_name == item_code){
									check = 1
									cur_frm.doc.taxes[row].tax_amount = biaya
								}
							}
							if(check == 0){
								console.log("123")
								var d = frappe.model.add_child(cur_frm.doc, "Sales Taxes and Charges", "taxes")
								d.charge_type = "Actual"
								d.account_head = account
								d.item_name = item_code
								d.tax_amount = biaya
								d.description = "Biaya Item"
							}
							
							cur_frm.refresh_fields("taxes")
							frm.refresh_fields()
						}
					} 
				}
			})
		}
	}
});


frappe.ui.form.on('Sales Invoice', {
	refresh(frm) {
		// your code here
	},
})