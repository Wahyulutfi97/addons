cur_frm.cscript.custom_customer_name = function(doc){
	if(doc.customer_name){
		doc.customer_name = doc.customer_name.charAt(0).toUpperCase() + doc.customer_name.slice(1)
		refresh_field("customer_name")
	}
}