#!/usr/bin/env python3
"""Minimal fill test - just fill a few basic fields"""

from fillpdf import fillpdfs

INPUT_PDF = "/home/user/PDF_HELP/TEMPLATES/ACH_AUTH.pdf"
OUTPUT_PDF = "/home/user/PDF_HELP/test/ACH_FILLED_TEST.pdf"

# Minimal test data
data = {
    "schwab_holder_1": "JOHN DOE",
    "schwab_holder_ssn": "123-45-6789",
    "schwab_account_numbers": "1234-5678",
    "schwab_sig_1_print": "JOHN DOE",
}

print("Filling PDF...")
fillpdfs.write_fillable_pdf(INPUT_PDF, OUTPUT_PDF, data)
print(f"Written to: {OUTPUT_PDF}")

# Verify by reading back
print("\n=== Verifying filled fields ===")
fields = fillpdfs.get_form_fields(OUTPUT_PDF)
for key in data.keys():
    print(f"{key}: '{fields.get(key, 'NOT FOUND')}'")
