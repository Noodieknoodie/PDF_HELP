#!/usr/bin/env python3
"""Test checkbox and radio button fields"""

from fillpdf import fillpdfs

INPUT_PDF = "/home/user/PDF_HELP/TEMPLATES/ACH_AUTH.pdf"
OUTPUT_PDF = "/home/user/PDF_HELP/test/ACH_CHECKBOX_TEST.pdf"

# Test data with checkboxes and radio buttons
data = {
    # Text fields
    "schwab_holder_1": "JANE SMITH",
    "schwab_holder_ssn": "987-65-4321",
    "schwab_account_numbers": "9999-8888",

    # Checkbox (from instructions: acct_type_personal_checking)
    "acct_type_personal_checking": True,

    # Radio button (from instructions: is_owner_external with values /Yes, /No)
    "is_owner_external": "Yes",

    # Another checkbox
    "tx_new_request": True,
}

print("Filling PDF with checkboxes...")
fillpdfs.write_fillable_pdf(INPUT_PDF, OUTPUT_PDF, data)
print(f"Written to: {OUTPUT_PDF}")

# Verify
print("\n=== Verifying ===")
fields = fillpdfs.get_form_fields(OUTPUT_PDF)
for key in data.keys():
    print(f"{key}: '{fields.get(key, 'NOT FOUND')}'")
