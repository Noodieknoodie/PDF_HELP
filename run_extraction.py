import os
from datetime import datetime
from PyPDF2 import PdfReader

def extract_pdf_fields(pdf_path, output_path):
    """Extract form fields from a PDF and write to a text file."""
    try:
        reader = PdfReader(pdf_path)
        all_fields = reader.get_fields()

        items = []
        if all_fields:
            for name, obj in all_fields.items():
                ftype = "Unknown"
                if "/FT" in obj:
                    t = obj["/FT"]
                    if t == "/Tx":
                        ftype = "Text"
                    elif t == "/Ch":
                        ftype = "Choice"
                    elif t == "/Sig":
                        ftype = "Signature"
                    elif t == "/Btn":
                        flags = obj.get("/Ff", 0)
                        if flags & 65536:
                            ftype = "Radio"
                        elif flags & 131072:
                            ftype = "Push"
                        else:
                            ftype = "Checkbox"

                items.append((name, ftype))

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"Source: {os.path.basename(pdf_path)}\n")
            f.write(f"Date: {datetime.now():%Y-%m-%d %H:%M}\n")
            f.write(f"Total fields: {len(items)}\n\n")
            f.write("ID, Field Name, Type\n")

            for i, (name, ftype) in enumerate(items, 1):
                f.write(f"{i}, {name}, {ftype}\n")

        print(f"✓ {os.path.basename(pdf_path)}: {len(items)} fields extracted")
        return len(items)

    except Exception as e:
        print(f"✗ {os.path.basename(pdf_path)}: Error - {e}")
        return 0

# List of PDF files to process
pdf_files = [
    "529_App.pdf",
    "Acct_Personal.pdf",
    "Acct_Trust.pdf",
    "ACH_AUTH.pdf",
    "Bene_Designation.pdf",
    "ChangeofAddress.pdf",
    "IMA.pdf",
    "IRA_Acct_App.pdf",
    "IRA_RO_Designation.pdf",
    "LPOA.pdf",
    "Options_Trading_Margin.pdf",
    "Trading_Withdrawal_Authorization.pdf",
    "Transfer_of_Account.pdf",
    "Wire_Transfer.pdf"
]

# Process all PDFs
templates_dir = "TEMPLATES"
outputs_dir = "OUTPUTS"
os.makedirs(outputs_dir, exist_ok=True)

print("Extracting form fields from PDF templates...")
print("=" * 50)

success_count = 0
total_fields = 0

for pdf_file in pdf_files:
    pdf_path = os.path.join(templates_dir, pdf_file)
    output_filename = pdf_file.replace('.pdf', '_fields.txt')
    output_path = os.path.join(outputs_dir, output_filename)
    
    if os.path.exists(pdf_path):
        field_count = extract_pdf_fields(pdf_path, output_path)
        if field_count > 0:
            success_count += 1
            total_fields += field_count
    else:
        print(f"✗ {pdf_file}: File not found")

print("=" * 50)
print(f"Summary:")
print(f"  Files processed: {success_count}/{len(pdf_files)}")
print(f"  Total fields: {total_fields}")
print(f"  Output location: {outputs_dir}/")
print("\nExtraction complete!")