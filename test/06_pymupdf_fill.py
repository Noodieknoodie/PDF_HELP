#!/usr/bin/env python3
"""Use PyMuPDF (fitz) directly for proper form filling with visual appearance"""

import fitz  # pymupdf

INPUT_PDF = "/home/user/PDF_HELP/TEMPLATES/ACH_AUTH.pdf"
OUTPUT_PDF = "/home/user/PDF_HELP/test/ACH_PYMUPDF_FILLED.pdf"

# Test data
data = {
    "schwab_holder_1": "JOHN DOE & JANE DOE",
    "schwab_holder_ssn": "123-45-6789",
    "schwab_account_numbers": "1234-5678",
    "aba_routing": "021000021",
    "external_account_number": "987654321",
    "external_account_name": "JOHN DOE",
    "external_bank_name": "CHASE BANK",
    "schwab_sig_1_print": "JOHN DOE",
}

doc = fitz.open(INPUT_PDF)

# Iterate through pages and fill fields
for page in doc:
    # Get all widgets (form fields) on this page
    for widget in page.widgets():
        field_name = widget.field_name
        if field_name in data:
            widget.field_value = data[field_name]
            widget.update()
            print(f"Filled: {field_name} = {data[field_name]}")

# Save with appearance streams updated
doc.save(OUTPUT_PDF)
doc.close()

print(f"\nSaved to: {OUTPUT_PDF}")

# Verify by reopening
print("\n=== Verification ===")
doc = fitz.open(OUTPUT_PDF)
for page in doc:
    for widget in page.widgets():
        if widget.field_name in data:
            print(f"{widget.field_name}: {widget.field_value}")
doc.close()
