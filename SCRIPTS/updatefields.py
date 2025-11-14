import os
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import NameObject, TextStringObject, BooleanObject

RENAME = {
    "DA1":"disc_acct_num_1",
    "DA2":"disc_acct_num_2",
    "DA3":"disc_acct_num_3",
    "DA4":"disc_acct_num_4",
    "DF1":"disc_fee_1",
    "DF2":"disc_fee_2",
    "DF3":"disc_fee_3",
    "DF4":"disc_fee_4",
    "DIS1":"disc_strategy_1",
    "DIS2":"disc_strategy_2",
    "DIS3":"disc_strategy_3",
    "DIS4":"disc_strategy_4",
    "NA1":"nondisc_acct_num_1",
    "NA2":"nondisc_acct_num_2",
    "NA3":"nondisc_acct_num_3",
    "NA4":"nondisc_acct_num_4",
    "NF1":"nondisc_fee_1",
    "NF2":"nondisc_fee_2",
    "NF3":"nondisc_fee_3",
    "NF4":"nondisc_fee_4",
    "NIS1":"nondisc_strategy_1",
    "NIS2":"nondisc_strategy_2",
    "NIS3":"nondisc_strategy_3",
    "NIS4":"nondisc_strategy_4",
    "Fax":"advisor_fax",
    "Advisor Name":"advisor_name",
    "Client 1 Name":"client1_name",
    "Client 2 Name":"client2_name",
    "&":"client_connector_amp",
    "Client 1 Address":"client1_address_1",
    "Client 1 Address 2":"client1_address_2",
    "Client 1 Phone":"client1_phone",
    "Advisor Phone Number":"advisor_phone",
    "Client 2 Address 2":"client2_address_2",
    "Client 2 Phone":"client2_phone",
    "Client 2 Address":"client2_address_1",
    "CD1":"misc_cd1",
    "Hide":"hide_toggle",
    "Date":"date_effective",
    "Year":"year_effective",
    "Custodian1":"custodian_dropdown",
    "LevelTax Considerations":"tax_considerations",
    "LevelRegulatory Requirements":"regulatory_requirements",
    "LevelUnique Circumstances":"unique_circumstances",
    "Client Communication":"client_communication",
    "Equities":"equities_notes",
    "Equity Restrictions":"equity_restrictions",
    "Fixed Income":"fixed_income_notes",
    "Return Objective":"return_objective",
    "Investment Style":"investment_style",
    "Time Horizon":"time_horizon",
    "Liquidity Needs":"liquidity_needs",
    "Asset Allocation":"asset_allocation",
    "Check Box2":"alt_checkbox",
    "Text5":"misc_text5",
    "Text1":"misc_text1",
    "Text2":"misc_text2",
}

INPUT = r"C:\Users\ErikKnudsen\OneDrive - Hohimer Wealth Management\Documents\Prefilled-Forms\TEMPLATES\IMA_FORM_BLANK.pdf"
OUTPUT = r"C:\Users\ErikKnudsen\OneDrive - Hohimer Wealth Management\Documents\Prefilled-Forms\output\IMA_RENAMED.pdf"

def clean_name(x):
    return str(x).strip()

def rename_field_dict(field_obj):
    if hasattr(field_obj, "get_object"):
        field = field_obj.get_object()
    else:
        field = field_obj

    if "/T" in field:
        old_raw = field["/T"]
        old = clean_name(old_raw)
        if old in RENAME:
            field[NameObject("/T")] = TextStringObject(RENAME[old])

    kids = field.get("/Kids")
    if kids:
        for kid in kids:
            rename_field_dict(kid)

def rename_fields():
    reader = PdfReader(INPUT)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    root = reader.trailer["/Root"]
    acro_raw = root.get("/AcroForm")
    if not acro_raw:
        with open(OUTPUT, "wb") as f_out:
            writer.write(f_out)
        return

    acroform = acro_raw.get_object() if hasattr(acro_raw, "get_object") else acro_raw

    fields = acroform.get("/Fields", [])
    for field in fields:
        rename_field_dict(field)

    acroform[NameObject("/NeedAppearances")] = BooleanObject(True)
    writer._root_object.update({NameObject("/AcroForm"): writer._add_object(acroform)})

    with open(OUTPUT, "wb") as f_out:
        writer.write(f_out)

if __name__ == "__main__":
    rename_fields()
