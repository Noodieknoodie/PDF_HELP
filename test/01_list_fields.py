#!/usr/bin/env python3
"""Step 1: List all fields in the PDF to verify field names"""

from pypdf import PdfReader

pdf_path = "/home/user/PDF_HELP/TEMPLATES/ACH_AUTH.pdf"
reader = PdfReader(pdf_path)

print(f"PDF has {len(reader.pages)} pages")
print("\n=== FORM FIELDS ===\n")

fields = reader.get_fields()
if fields:
    for name, field in fields.items():
        field_type = field.get('/FT', 'Unknown')
        value = field.get('/V', '')
        print(f"Field: {name}")
        print(f"  Type: {field_type}")
        if value:
            print(f"  Current Value: {value}")
        print()
else:
    print("No form fields found!")
