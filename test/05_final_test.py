#!/usr/bin/env python3
"""Full test with flattening to verify visual output"""

from fillpdf import fillpdfs
import fitz  # pymupdf

INPUT_PDF = "/home/user/PDF_HELP/TEMPLATES/ACH_AUTH.pdf"
OUTPUT_FILLABLE = "/home/user/PDF_HELP/test/ACH_FINAL_FILLABLE.pdf"
OUTPUT_FLAT = "/home/user/PDF_HELP/test/ACH_FINAL_FLAT.pdf"

# Test data
data = {
    # Section 1: Schwab Account Info
    "schwab_holder_1": "JOHN DOE & JANE DOE",
    "schwab_holder_ssn": "123-45-6789",
    "schwab_account_numbers": "1234-5678",

    # Section 3: External bank info
    "aba_routing": "021000021",
    "external_account_number": "123456789",
    "external_account_name": "JOHN DOE",
    "external_bank_name": "CHASE BANK",
    "acct_type_personal_checking": True,

    # Radio buttons
    "is_owner_external": "Yes",
    "is_identity_match": "Yes_2",

    # Section 2: Transaction type
    "tx_new_request": True,

    # Section 7: Signatures
    "schwab_sig_1_print": "JOHN DOE",
}

print("Step 1: Write fillable PDF...")
fillpdfs.write_fillable_pdf(INPUT_PDF, OUTPUT_FILLABLE, data)

print("Step 2: Flatten PDF (bake in values)...")
fillpdfs.flatten_pdf(OUTPUT_FILLABLE, OUTPUT_FLAT)

print("\nStep 3: Verify with PyMuPDF...")
doc = fitz.open(OUTPUT_FLAT)
# Extract text from first page to verify
page = doc[1]  # Page 2 (0-indexed) has the data
text = page.get_text()
doc.close()

# Check for our values in the text
checks = ["JOHN DOE", "123-45-6789", "1234-5678", "021000021"]
print("\nVerification:")
for check in checks:
    found = check in text
    print(f"  '{check}' in PDF: {found}")

print(f"\nOutput files:")
print(f"  Fillable: {OUTPUT_FILLABLE}")
print(f"  Flattened: {OUTPUT_FLAT}")
