#!/usr/bin/env python3
"""Step 1: List all fields using fillpdf"""

from fillpdf import fillpdfs

pdf_path = "/home/user/PDF_HELP/TEMPLATES/ACH_AUTH.pdf"

print("=== Listing all form fields ===\n")
fields = fillpdfs.get_form_fields(pdf_path)

for name, value in fields.items():
    print(f"{name}: '{value}'")
