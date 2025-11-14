"""
Schwab Account Application Filler
Clean production version for renamed field PDF
"""

import fitz  # PyMuPDF
import os
from datetime import datetime

def fill_schwab_application():
    """Fill Schwab account application with test data"""
    
    # File paths
    template_path = r"C:\Users\ErikKnudsen\OneDrive - Hohimer Wealth Management\Documents\Prefilled-Forms\TEMPLATES\Account_App_Personal_blank.pdf"
    output_dir = r"C:\Users\ErikKnudsen\OneDrive - Hohimer Wealth Management\Documents\Prefilled-Forms\output"
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate timestamped output filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_dir, f"schwab_application_{timestamp}.pdf")
    
    # Test data
    form_data = {
        # IA Information
        "ia_firm_name": "HOHIMER WEALTH MANAGEMENT",
        "ia_master_account": "7890-1234",
        "service_team": "SEATTLE TEAM",
        "ia_contact_name": "JOHN ADVISOR",
        "ia_phone": "206-555-0100",
        "ia_email": "advisor@hohimer.com",
        "firm_is_custodian": False,
        "firm_holds_other_assets": False,
        
        # Account Type
        "account_type_schwab_one": True,
        "account_type_margin": False,
        
        # Registration
        "reg_individual": True,
        "reg_joint_rights": False,
        "reg_tenants_common": False,
        "reg_tenants_entirety": False,
        "reg_community_property": False,
        "reg_community_rights": False,
        "reg_conservatorship": False,
        "reg_guardianship": False,
        "reg_custodial": False,
        "reg_estate": False,
        
        # Primary Account Holder
        "primary_first_name": "ROBERT",
        "primary_middle_name": "JAMES",
        "primary_last_name": "THOMPSON",
        "primary_suffix": "JR",
        "primary_ssn": "123-45-6789",
        "primary_dob": "03/15/1975",
        "primary_preferred_name": "BOB",
        "primary_street_address": "123 PINE STREET APT 4B",
        "primary_city": "SEATTLE",
        "primary_state": "WA",
        "primary_zip": "98101",
        "primary_country": "USA",
        "primary_phone": "206-555-0200",
        "primary_mobile": "206-555-0201",
        "primary_email": "bob.thompson@example.com",
        "primary_mothers_maiden": "JOHNSON",
        
        # Primary Citizenship/ID
        "primary_citizen_usa": True,
        "primary_citizen_other": False,
        "primary_residence_usa": True,
        "primary_residence_other": False,
        "primary_id_license": True,
        "primary_id_passport": False,
        "primary_id_govt": False,
        "primary_id_number": "WA123456789",
        "primary_id_state": "WA",
        "primary_id_issue_date": "01/15/2020",
        "primary_id_exp_date": "03/15/2028",
        
        # Employment
        "primary_employment_employed": True,
        "primary_employment_retired": False,
        "primary_occupation_it": True,
        "primary_employer_name": "MICROSOFT CORPORATION",
        "primary_employer_address": "1 MICROSOFT WAY",
        "primary_employer_city": "REDMOND",
        "primary_employer_state": "WA",
        "primary_employer_zip": "98052",
        "primary_employer_country": "USA",
        
        # Regulatory
        "primary_finra_no": True,
        "primary_finra_yes": False,
        "primary_director_no": True,
        "primary_director_yes": False,
        
        # Trusted Contact 1
        "trust_contact1_first": "SARAH",
        "trust_contact1_last": "THOMPSON",
        "trust_contact1_rel_spouse": True,
        "trust_contact1_address": "123 PINE STREET APT 4B",
        "trust_contact1_city": "SEATTLE",
        "trust_contact1_state": "WA",
        "trust_contact1_zip": "98101",
        "trust_contact1_country": "USA",
        "trust_contact1_phone": "206-555-0202",
        
        # Source of Funds
        "source_salary": True,
        "source_capital_gains": True,
        "source_inheritance": False,
        
        # Purpose of Account
        "purpose_general": True,
        "purpose_retirement": True,
        
        # Checking Preferences
        "checks_one_card": True,
        "activity_medium": True,
        
        # IA Authorizations
        "auth_trading_disbursement": True,
        "auth_fee_payment": True,
        
        # Signature
        "primary_print_name": "ROBERT JAMES THOMPSON JR",
        "primary_sign_date": datetime.now().strftime("%m/%d/%Y"),
    }
    
    # Open and fill the PDF
    try:
        doc = fitz.open(template_path)
        filled_count = 0
        failed_fields = []
        
        # Process all pages
        for page in doc:
            for widget in page.widgets():
                field_name = widget.field_name
                
                if field_name in form_data:
                    try:
                        value = form_data[field_name]
                        
                        # Handle checkboxes vs text fields
                        if widget.field_type == fitz.PDF_WIDGET_TYPE_CHECKBOX:
                            widget.field_value = bool(value)
                        else:
                            widget.field_value = str(value)
                        
                        widget.update()
                        filled_count += 1
                        
                    except Exception as e:
                        failed_fields.append((field_name, str(e)))
        
        # Save the filled PDF
        doc.save(output_path)
        doc.close()
        
        # Report results
        print(f"✓ Filled {filled_count} fields successfully")
        if failed_fields:
            print(f"✗ Failed to fill {len(failed_fields)} fields:")
            for field, error in failed_fields[:5]:  # Show first 5 failures
                print(f"  - {field}: {error}")
        
        print(f"\nSaved to: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = fill_schwab_application()
    if success:
        print("\n✅ Form filled successfully!")
    else:
        print("\n❌ Form filling failed")