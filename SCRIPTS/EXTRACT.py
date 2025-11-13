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

        field_list = []
        for field_name, field_object in all_fields.items():
            if '/FT' in field_object:
                field_type_code = field_object['/FT']
                type_mapping = {
                    '/Tx': 'Text',
                    '/Btn': 'Button',
                    '/Ch': 'Choice',
                    '/Sig': 'Signature'
                }
                field_type = type_mapping.get(field_type_code, str(field_type_code))
                if field_type_code == '/Btn':
                    flags = field_object.get('/Ff', 0)
                    if flags & 65536:
                        field_type = 'Radio'
                    elif flags & 131072:
                        field_type = 'Push'
                    else:
                        field_type = 'Checkbox'
                field_list.append((field_name, field_type))

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"Source: {os.path.basename(pdf_path)}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"Total fields: {len(field_list)}\n\n")
            f.write("ID, Field Name, Type\n")
            for i, (field_name, field_type) in enumerate(field_list, start=1):
                f.write(f"{i}, {field_name}, {field_type}\n")

        return len(field_list)

    except Exception:
        return 0

def main():
    input_dir = r"C:\Users\ErikKnudsen\OneDrive - Hohimer Wealth Management\Documents\Prefilled-Forms\input"
    output_dir = r"C:\Users\ErikKnudsen\OneDrive - Hohimer Wealth Management\Documents\Prefilled-Forms\output"
    os.makedirs(output_dir, exist_ok=True)

    pdf_files = glob.glob(os.path.join(input_dir, "*.pdf"))
    if not pdf_files:
        return

    total_fields = 0
    for pdf_path in pdf_files:
        pdf_name = os.path.basename(pdf_path)
        output_filename = pdf_name.replace('.pdf', '_fields.txt')
        output_path = os.path.join(output_dir, output_filename)
        fields_count = extract_pdf_fields(pdf_path, output_path)
        total_fields += fields_count

if __name__ == "__main__":
    main()
