"""
Schwab Account Application PDF Filler - Test Script
Fills a blank Schwab One Account Application with test data
"""

import os
from datetime import datetime
from pypdf import PdfReader, PdfWriter

def fill_schwab_application():
    """Fill Schwab account application with test data"""
    
    # Define paths
    template_path = r"C:\Users\ErikKnudsen\OneDrive - Hohimer Wealth Management\Documents\Prefilled-Forms\TEMPLATES\Account_App_Personal_blank.pdf"
    output_dir = r"C:\Users\ErikKnudsen\OneDrive - Hohimer Wealth Management\Documents\Prefilled-Forms\output"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate output filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_dir, f"schwab_application_test_{timestamp}.pdf")
    
    # Test data dictionary - mixing various field types and sections
    test_data = {
        # Investment Advisor Information
        "ia_firm_name": "HOHIMER WEALTH MANAGEMENT",
        "ia_master_account": "7890-1234",
        "service_team": "SEATTLE TEAM",
        "ia_contact_name": "JOHN ADVISOR",
        "ia_phone": "206-555-0100",
        "ia_email": "advisor@hohimer.com",
        "firm_is_custodian": "/Off",  # Checkbox unchecked
        
        # Account Type
        "account_type_schwab_one": "/Yes",  # Checkbox checked
        "account_type_margin": "/Off",
        
        # Registration Type - Individual account for this test
        "reg_individual": "/Yes",
        "reg_joint_rights": "/Off",
        "reg_tenants_common": "/Off",
        
        # Primary Account Holder
        "primary_first_name": "ROBERT",
        "primary_middle_name": "JAMES",
        "primary_last_name": "THOMPSON",
        "primary_suffix": "JR",
        "primary_ssn": "123-45-6789",
        "primary_dob": "03/15/1975",
        "primary_preferred_name": "BOB",
        
        # Primary Address
        "primary_street_address": "123 PINE STREET APT 4B",
        "primary_city": "SEATTLE",
        "primary_state": "WA",
        "primary_zip": "98101",
        "primary_country": "USA",
        
        # Primary Contact
        "primary_phone": "206-555-0200",
        "primary_mobile": "206-555-0201",
        "primary_email": "bob.thompson@email.com",
        "primary_mothers_maiden": "JOHNSON",
        
        # Primary Citizenship/Residence
        "primary_citizen_usa": "/Yes",
        "primary_citizen_other": "/Off",
        "primary_residence_usa": "/Yes",
        "primary_residence_other": "/Off",
        
        # Primary ID
        "primary_id_license": "/Yes",
        "primary_id_passport": "/Off",
        "primary_id_govt": "/Off",
        "primary_id_number": "WA123456789",
        "primary_id_state": "WA",
        "primary_id_issue_date": "01/15/2020",
        "primary_id_exp_date": "03/15/2028",
        
        # Primary Employment
        "primary_employment_employed": "/Yes",
        "primary_employment_self": "/Off",
        "primary_employment_retired": "/Off",
        "primary_occupation_it": "/Yes",
        "primary_occupation_executive": "/Off",
        "primary_employer_name": "MICROSOFT CORPORATION",
        "primary_employer_address": "1 MICROSOFT WAY",
        "primary_employer_city": "REDMOND",
        "primary_employer_state": "WA",
        "primary_employer_zip": "98052",
        "primary_employer_country": "USA",
        
        # Regulatory
        "primary_finra_no": "/Yes",
        "primary_finra_yes": "/Off",
        "primary_director_no": "/Yes",
        "primary_director_yes": "/Off",
        
        # Trusted Contact Person 1
        "trust_contact1_first": "SARAH",
        "trust_contact1_last": "THOMPSON",
        "trust_contact1_rel_spouse": "/Yes",
        "trust_contact1_rel_friend": "/Off",
        "trust_contact1_address": "123 PINE STREET APT 4B",
        "trust_contact1_city": "SEATTLE",
        "trust_contact1_state": "WA",
        "trust_contact1_zip": "98101",
        "trust_contact1_country": "USA",
        "trust_contact1_phone": "206-555-0202",
        "trust_contact1_email": "sarah.thompson@email.com",
        
        # Trusted Contact Person 2
        "trust_contact2_first": "MICHAEL",
        "trust_contact2_middle": "ALAN",
        "trust_contact2_last": "THOMPSON",
        "trust_contact2_rel_sibling": "/Yes",
        "trust_contact2_address": "456 OAK AVENUE",
        "trust_contact2_city": "BELLEVUE",
        "trust_contact2_state": "WA",
        "trust_contact2_zip": "98004",
        "trust_contact2_mobile": "425-555-0300",
        
        # Paperless
        "paperless_opt_out": "/Off",  # Will receive electronic docs
        
        # Source of Funds (multiple)
        "source_salary": "/Yes",
        "source_capital_gains": "/Yes",
        "source_inheritance": "/Off",
        "source_gifts": "/Off",
        
        # Purpose of Account (multiple)
        "purpose_general": "/Yes",
        "purpose_retirement": "/Yes",
        "purpose_estate": "/Off",
        
        # Checking Preferences
        "checks_one_card": "/Yes",
        "checks_only": "/Off",
        "checks_two_cards": "/Off",
        "activity_medium": "/Yes",
        "activity_low": "/Off",
        "activity_high": "/Off",
        
        # IA Authorizations
        "auth_trading_disbursement": "/Yes",
        "auth_fee_payment": "/Yes",
        
        # Signature section
        "primary_print_name": "ROBERT JAMES THOMPSON JR",
        "primary_sign_date": datetime.now().strftime("%m/%d/%Y"),
    }
    
    try:
        # Read the template PDF
        print(f"Reading template from: {template_path}")
        reader = PdfReader(template_path)
        writer = PdfWriter()
        
        # Copy all pages and get form fields
        for page in reader.pages:
            writer.add_page(page)
        
        # Update form fields
        print("Filling form fields...")
        writer.update_page_form_field_values(
            writer.pages[0], 
            test_data
        )
        
        # For multi-page forms, you might need to update fields on other pages
        # Check if there are fields on other pages and update them
        for i, page in enumerate(writer.pages[1:], 1):
            try:
                writer.update_page_form_field_values(page, test_data)
            except:
                pass  # Some pages might not have form fields
        
        # Write the filled PDF
        print(f"Saving filled PDF to: {output_path}")
        with open(output_path, "wb") as output_file:
            writer.write(output_file)
        
        print(f"✓ Successfully created filled PDF: {output_path}")
        
        # Print summary of what was filled
        print("\n--- FILLED SECTIONS SUMMARY ---")
        print("✓ Investment Advisor Information")
        print("✓ Account Type: Individual Schwab One")
        print("✓ Primary Account Holder: Robert James Thompson Jr")
        print("✓ Address: Seattle, WA")
        print("✓ Employment: Microsoft Corporation (IT)")
        print("✓ 2 Trusted Contacts added")
        print("✓ Electronic documents selected")
        print("✓ Checking with 1 Visa card, medium activity")
        print("✓ Trading & Fee Payment authorizations")
        
    except FileNotFoundError:
        print(f"❌ Error: Template file not found at {template_path}")
        print("Please check the file path and ensure the file exists.")
    except PermissionError:
        print(f"❌ Error: Permission denied. Check file/folder permissions.")
    except Exception as e:
        print(f"❌ Error filling PDF: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        
        # If pypdf doesn't work, suggest alternative approach
        print("\n--- Alternative Approach ---")
        print("If pypdf isn't working, you can try:")
        print("1. Install fillpdf: pip install fillpdf")
        print("2. Or use pdfrw: pip install pdfrw")


def install_requirements():
    """Print installation instructions"""
    print("--- INSTALLATION REQUIRED ---")
    print("Run this command to install the required library:")
    print("pip install pypdf")
    print("\nOr if you prefer an alternative:")
    print("pip install fillpdf")
    print("pip install pdfrw")


if __name__ == "__main__":
    try:
        import pypdf
        fill_schwab_application()
    except ImportError:
        install_requirements()
        print("\nAfter installing, run this script again.")