import sys
import os
from datetime import datetime
from PyPDF2 import PdfReader

def extract_pdf_fields(pdf_path, output_path):
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

        print(f"Success: Extracted {len(items)} fields from {os.path.basename(pdf_path)}")
        return len(items)

    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return 0

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python process_single.py <input_pdf> <output_txt>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_path = sys.argv[2]
    
    extract_pdf_fields(pdf_path, output_path)