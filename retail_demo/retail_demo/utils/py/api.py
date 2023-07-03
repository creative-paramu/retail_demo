import frappe
from frappe.utils import nowdate
import json
import datetime
from datetime import timedelta
from datetime import date
@frappe.whitelist( allow_guest=True)
def customer_list():
    cus_list=frappe.db.get_all("Customer",pluck='name')
    frappe.local.response['Customer']=cus_list

@frappe.whitelist(allow_guest=True)
def sales_invoice(cus_name,items):
    items=json.loads(items)
    doc=frappe.new_doc("Sales Invoice")
    doc.update(
        {
            "customer":cus_name,
            "due_date": nowdate(),
            "items":items,
        })
    doc.flags.ignore_permissions = True
    try:
        doc.save()
        frappe.db.commit()
        frappe.local.response["message"] = "Invoice saved Successfully"
    except frappe.ValidationError as e:
        frappe.local.response.http_status_code = 417
        frappe.local.response["message"] = e