import frappe
from pyqrcode import create as qr_create
import io
import os
import json

@frappe.whitelist()
def after_insert(doc, event):
    # QR Generation
    data = [{"item_name": doc.item_name, "item_code": doc.item_code, "rate": doc.standard_rate, "qty": 1}]
    data = json.dumps(data)
    qr_image = io.BytesIO()
    data_ = qr_create(data, error='L')
    data_.png(qr_image, scale=5, quiet_zone=1)
    name = frappe.generate_hash('', 5)

    new_file = frappe.get_doc({
        "doctype": "File",
        "file_name": f"QRCode-{name}.png".replace(os.path.sep, "__"),
        "is_private": 0,
        "content": qr_image.getvalue(),
        "attached_to_doctype":  doc.doctype, 
        "attached_to_name": doc.name
    })
    new_file.save(ignore_permissions=True)
    doc.ts_qr_code = new_file.file_url
    doc.save()
