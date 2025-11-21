#!/bin/bash

# Create OUTPUTS directory if it doesn't exist
mkdir -p OUTPUTS

# Process each PDF file
echo "Processing PDF files..."
echo "========================"

# Process 529_App.pdf
echo "Processing 529_App.pdf..."
python3 process_single.py TEMPLATES/529_App.pdf OUTPUTS/529_App_fields.txt

# Process Acct_Personal.pdf
echo "Processing Acct_Personal.pdf..."
python3 process_single.py TEMPLATES/Acct_Personal.pdf OUTPUTS/Acct_Personal_fields.txt

# Process Acct_Trust.pdf
echo "Processing Acct_Trust.pdf..."
python3 process_single.py TEMPLATES/Acct_Trust.pdf OUTPUTS/Acct_Trust_fields.txt

# Process ACH_AUTH.pdf
echo "Processing ACH_AUTH.pdf..."
python3 process_single.py TEMPLATES/ACH_AUTH.pdf OUTPUTS/ACH_AUTH_fields.txt

# Process Bene_Designation.pdf
echo "Processing Bene_Designation.pdf..."
python3 process_single.py TEMPLATES/Bene_Designation.pdf OUTPUTS/Bene_Designation_fields.txt

# Process ChangeofAddress.pdf
echo "Processing ChangeofAddress.pdf..."
python3 process_single.py TEMPLATES/ChangeofAddress.pdf OUTPUTS/ChangeofAddress_fields.txt

# Process IMA.pdf
echo "Processing IMA.pdf..."
python3 process_single.py TEMPLATES/IMA.pdf OUTPUTS/IMA_fields.txt

# Process IRA_Acct_App.pdf
echo "Processing IRA_Acct_App.pdf..."
python3 process_single.py TEMPLATES/IRA_Acct_App.pdf OUTPUTS/IRA_Acct_App_fields.txt

# Process IRA_RO_Designation.pdf
echo "Processing IRA_RO_Designation.pdf..."
python3 process_single.py TEMPLATES/IRA_RO_Designation.pdf OUTPUTS/IRA_RO_Designation_fields.txt

# Process LPOA.pdf
echo "Processing LPOA.pdf..."
python3 process_single.py TEMPLATES/LPOA.pdf OUTPUTS/LPOA_fields.txt

# Process Options_Trading_Margin.pdf
echo "Processing Options_Trading_Margin.pdf..."
python3 process_single.py TEMPLATES/Options_Trading_Margin.pdf OUTPUTS/Options_Trading_Margin_fields.txt

# Process Trading_Withdrawal_Authorization.pdf
echo "Processing Trading_Withdrawal_Authorization.pdf..."
python3 process_single.py TEMPLATES/Trading_Withdrawal_Authorization.pdf OUTPUTS/Trading_Withdrawal_Authorization_fields.txt

# Process Transfer_of_Account.pdf
echo "Processing Transfer_of_Account.pdf..."
python3 process_single.py TEMPLATES/Transfer_of_Account.pdf OUTPUTS/Transfer_of_Account_fields.txt

# Process Wire_Transfer.pdf
echo "Processing Wire_Transfer.pdf..."
python3 process_single.py TEMPLATES/Wire_Transfer.pdf OUTPUTS/Wire_Transfer_fields.txt

echo "========================"
echo "Processing complete!"
echo "Check the OUTPUTS folder for the generated text files."