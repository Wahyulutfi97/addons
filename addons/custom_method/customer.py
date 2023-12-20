import frappe
from frappe.model.naming import make_autoname

@frappe.whitelist()
def autoname_customer_and_serial(self,method):
    self.name = self.get_customer_name()
    self.serial_customer = make_autoname("CUST-.YY.MM.DD.-.#####")
    if frappe.db.get_value("Customer", { 'customer_name' : self.name, 'nomor_whatsapp_l' : self.nomor_whatsapp_l}):
        frappe.throw("Nama [{}] dengan kontak [{}] telah digunakan".format(self.name, self.nomor_whatsapp_l))

    total = frappe.db.count('Customer', { 'customer_name': self.customer_name })
    if total > 0:
        self.name = self.name + ' - {}'.format(total)
