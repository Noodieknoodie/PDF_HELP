import os
import glob
from PyPDF2 import PdfReader
from datetime import datetime

def extract_pdf_fields(pdf_path, output_path):
    try:
        reader = PdfReader(pdf_path)
        all_fields = reader.get_fields()
        if not all_fields:
            return 0

        items = []
        for name, obj in all_fields.items():
            ftype = "Unknown"
            if "/FT" in obj:
                t = obj["/FT"]
                if t == "/Tx": ftype = "Text"
                elif t == "/Ch": ftype = "Choice"
                elif t == "/Sig": ftype = "Signature"
                elif t == "/Btn":
                    flags = obj.get("/Ff", 0)
                    if flags & 65536: ftype = "Radio"
                    elif flags & 131072: ftype = "Push"
                    else: ftype = "Checkbox"

            opts = obj.get("/Opt", None)
            drop = []
            if opts:
                for o in opts:
                    if isinstance(o, list) and len(o) >= 2:
                        drop.append(str(o[1]))
                    else:
                        drop.append(str(o))

            items.append((name, ftype, drop))

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"Source: {os.path.basename(pdf_path)}\n")
            f.write(f"Date: {datetime.now():%Y-%m-%d %H:%M}\n")
            f.write(f"Total fields: {len(items)}\n\n")
            f.write("ID, Field Name, Type, Options\n")

            for i, (name, ftype, drop) in enumerate(items, 1):
                opts = "; ".join(drop) if drop else ""
                f.write(f"{i}, {name}, {ftype}, {opts}\n")

        return len(items)

    except Exception:
        return 0

def main():
    input_dir = r"C:\Users\ErikKnudsen\OneDrive - Hohimer Wealth Management\Documents\Prefilled-Forms\input"
    output_dir = r"C:\Users\ErikKnudsen\OneDrive - Hohimer Wealth Management\Documents\Prefilled-Forms\output"
    os.makedirs(output_dir, exist_ok=True)

    pdfs = glob.glob(os.path.join(input_dir, "*.pdf"))
    if not pdfs:
        return

    total = 0
    for p in pdfs:
        out = os.path.join(output_dir, os.path.basename(p).replace(".pdf", "_fields.txt"))
        total += extract_pdf_fields(p, out)

if __name__ == "__main__":
    main()
