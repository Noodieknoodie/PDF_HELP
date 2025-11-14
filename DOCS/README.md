# Financial Account Operations PDF Automation System

## Project Overview

This system automates the preparation of PDF documents for financial account operations at Hohimer Wealth Management. The primary goal is to streamline the creation of DocuSign packages for account openings, transfers, and related paperwork by automating the population of PDF forms based on client statements and minimal user input.

## Current Technical Foundation

### PDF Form Handling
- All PDF forms have been converted from XFA to AcroForm format using Adobe Acrobat
- Fields have been systematically renamed to snake_case conventions (e.g., `ia_firm_name`, `primary_first_name`)
- PyMuPDF (`fitz`) is the chosen library for reliable form population
- Field mappings are documented in `FIELD_NAMES.txt` files for each form type

### Technical Requirements
- Python with PyMuPDF library
- Forms require boolean values for checkboxes (True/False)
- Text fields accept string values
- Dates use mm/dd/yyyy format
- Names and addresses should be in CAPITAL LETTERS per financial form standards

## Project Structure

```
project_root/
├── scripts/                 # Pre-written population scripts
├── blank_source_docs/       # Template PDFs (with renamed fields)
├── outputs/                 # Generated filled PDFs
├── inputs/                  # YAML data files for form population
├── documentation/           # Detailed form field documentation
├── statements/              # Client statements (input)
├── task.md                  # User instructions to AI agent
└── claude.md               # System instructions for AI agent
```

## Planned Workflow

1. **User Input Phase**
   - User places client statements in `statements/`
   - User writes requirements in `task.md` (which accounts to open, transfer instructions, etc.)

2. **AI Agent Processing**
   - Parses statements to extract client data
   - Generates YAML files in `inputs/` (one per document needed)
   - Executes pre-written population scripts
   - Reports completion status

3. **Data Structure**
   - Core client data (SSN, names, addresses) shared across forms
   - Form-specific YAML for unique fields
   - Constant fields (advisor info) pre-filled in templates

## Implementation Status

### ✅ Completed
- PDF field renaming methodology
- PyMuPDF integration approach
- Basic file structure definition
- Field population technical requirements

### 📝 In Progress
- Field documentation for each form type
- Pre-written population scripts
- YAML data structure design

### 🔜 Upcoming Components

#### Decision Tree Logic
*[To be documented: Logic for determining which forms are needed based on source/destination custodians and account types]*

#### Form-Specific Business Rules
*[To be documented: Specific requirements, conditional fields, and validation rules for each form type]*

#### Statement Parsing Logic
*[To be documented: How to extract data from various custodian statement formats]*

#### Validation Rules
*[To be documented: Data validation and compliance requirements]*

## Key Design Decisions

1. **Pre-written Scripts**: Rather than having the AI generate Python code each time, we're using pre-written, tested population scripts that accept YAML input
2. **Constant Prefilling**: Advisor information and other constants are pre-filled in templates, reducing complexity and potential errors
3. **Modular Data**: Two-tier YAML system (core + form-specific) to minimize redundancy
4. **Minimal AI Code Writing**: AI agent focuses on data extraction and YAML generation, not script creation

## Security Considerations
- No storage of sensitive client data in code
- Advisor/firm constants isolated from AI system
- Clear separation between data and logic

## Notes
- This system is designed for internal use by operations team members
- All forms follow Schwab's formatting requirements unless otherwise specified
- System assumes familiarity with financial account transfer processes

---

*Last Updated: November 2025*  
*Version: 0.1.0 (Initial Documentation)*