#!/usr/bin/env python3
"""
IMA Form Field Renamer
Uses pypdf with TextStringObject for reliable field renaming
Based on our successful pattern from previous conversations
"""

from pypdf import PdfReader, PdfWriter
from pypdf.generic import TextStringObject
import json
import os
from datetime import datetime

def create_field_mapping():
    """Create the field mapping dictionary"""
    return {
        # Date fields - Deceased/Alternate
        "DA1": "deceased_alternate_date_1",
        "DA2": "deceased_alternate_date_2", 
        "DA3": "deceased_alternate_date_3",
        "DA4": "deceased_alternate_date_4",
        
        # Full name fields - Deceased
        "DF1": "deceased_full_name_1",
        "DF2": "deceased_full_name_2",
        "DF3": "deceased_full_name_3",
        "DF4": "deceased_full_name_4",
        
        # SSN fields - Deceased
        "DIS1": "deceased_ssn_1",
        "DIS2": "deceased_ssn_2",
        "DIS3": "deceased_ssn_3",
        "DIS4": "deceased_ssn_4",
        
        # Date fields - New/Active
        "NA1": "new_active_date_1",
        "NA2": "new_active_date_2",
        "NA3": "new_active_date_3",
        "NA4": "new_active_date_4",
        
        # Full name fields - New
        "NF1": "new_full_name_1",
        "NF2": "new_full_name_2",
        "NF3": "new_full_name_3",
        "NF4": "new_full_name_4",
        
        # SSN fields - New
        "NIS1": "new_ssn_1",
        "NIS2": "new_ssn_2",
        "NIS3": "new_ssn_3",
        "NIS4": "new_ssn_4",
        
        # Contact fields
        "Fax": "fax_number",
        "Advisor Name": "advisor_name",
        "Client 1 Name": "client_1_name",
        "Client 2 Name": "client_2_name",
        "&": "and_symbol",
        "Client 1 Address": "client_1_address",
        "Client 1 Address 2": "client_1_address_2",
        "Client 1 Phone": "client_1_phone",
        "Advisor Phone Number": "advisor_phone",
        "Client 2 Address 2": "client_2_address_2",
        "Client 2 Phone": "client_2_phone",
        "Client 2 Address": "client_2_address",
        
        # Other fields
        "CD1": "cd1_field",
        "Hide": "hide_option",
        "Date": "form_date",
        "Year": "form_year",
        "Custodian1": "custodian_selection",
        "LevelTax Considerations": "level_tax_considerations",
        "LevelRegulatory Requirements": "level_regulatory_requirements",
        "LevelUnique Circumstances": "level_unique_circumstances",
        "Client Communication": "client_communication",
        "Equities": "equities_allocation",
        "Equity Restrictions": "equity_restrictions",
        "Fixed Income": "fixed_income_allocation",
        "Return Objective": "return_objective",
        "Investment Style": "investment_style",
        "Time Horizon": "time_horizon",
        "Liquidity Needs": "liquidity_needs",
        "Asset Allocation": "asset_allocation",
        "Check Box2": "checkbox_2",
        "Text5": "text_field_5",
        "Text1": "text_field_1",
        "Text2": "text_field_2"
    }

def rename_pdf_fields(input_pdf, output_pdf):
    """
    Rename PDF fields using the proven pypdf pattern
    """
    # Get field mapping
    field_mapping = create_field_mapping()
    
    # Read the PDF
    reader = PdfReader(input_pdf)
    writer = PdfWriter()
    
    # Append all pages with form fields
    writer.append(reader)
    
    # Statistics
    renamed_count = 0
    unmapped_count = 0
    errors = []
    
    # Access and rename form fields
    try:
        if hasattr(writer, '_root_object') and writer._root_object:
            if "/AcroForm" in writer._root_object:
                acro_form = writer._root_object["/AcroForm"]
                if "/Fields" in acro_form:
                    fields = acro_form["/Fields"]
                    
                    print(f"Found {len(fields)} fields in PDF\n")
                    print("Renaming fields:")
                    print("-" * 50)
                    
                    for field_ref in fields:
                        try:
                            field = field_ref.get_object()
                            if "/T" in field:
                                old_name = str(field["/T"])
                                
                                if old_name in field_mapping:
                                    new_name = field_mapping[old_name]
                                    # Use TextStringObject for proper encoding
                                    field["/T"] = TextStringObject(new_name)
                                    print(f"✓ {old_name:30} → {new_name}")
                                    renamed_count += 1
                                else:
                                    print(f"⚠ No mapping for: {old_name}")
                                    unmapped_count += 1
                        except Exception as e:
                            errors.append(f"Field error: {e}")
                            
    except Exception as e:
        print(f"Error accessing form structure: {e}")
        return False
    
    # Save the output PDF
    try:
        with open(output_pdf, 'wb') as f:
            writer.write(f)
        print("\n" + "=" * 50)
        print(f"✓ Successfully renamed {renamed_count} fields")
        
        if unmapped_count > 0:
            print(f"⚠ {unmapped_count} fields had no mapping")
            
        if errors:
            print(f"⚠ {len(errors)} errors encountered:")
            for error in errors[:5]:  # Show first 5 errors
                print(f"  - {error}")
                
        print(f"\n✓ Output saved to: {output_pdf}")
        return True
        
    except Exception as e:
        print(f"Error saving PDF: {e}")
        return False

def main():
    """Main execution"""
    # File paths
    input_pdf = r"C:\Users\ErikKnudsen\OneDrive - Hohimer Wealth Management\Documents\Prefilled-Forms\TEMPLATES\IMA_FORM_BLANK.pdf"
    
    # Create timestamped output filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_pdf = r"C:\Users\ErikKnudsen\OneDrive - Hohimer Wealth Management\Documents\Prefilled-Forms\output\IMA_FORM_RENAMED_{}.pdf".format(timestamp)
    
    # Ensure output directory exists
    output_dir = os.path.dirname(output_pdf)
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 50)
    print("IMA Form Field Renamer")
    print("=" * 50)
    print(f"Input:  {input_pdf}")
    print(f"Output: {output_pdf}")
    print("=" * 50 + "\n")
    
    # Check if input file exists
    if not os.path.exists(input_pdf):
        print(f"❌ Error: Input file not found!")
        print(f"   Looking for: {input_pdf}")
        return
    
    # Rename the fields
    success = rename_pdf_fields(input_pdf, output_pdf)
    
    if success:
        print("\n✅ Process completed successfully!")
        print(f"   Your renamed PDF is ready at:")
        print(f"   {output_pdf}")
    else:
        print("\n❌ Process failed. Check errors above.")

if __name__ == "__main__":
    main()