#!/usr/bin/env python3

from pypdf import PdfReader, PdfWriter
from tkinter import filedialog, Tk

SOURCE_PDF = r"C:\Users\ErikKnudsen\OneDrive - Hohimer Wealth Management\Documents\Prefilled-Forms\ROLLOVER_FORM_BLANK.pdf"

client_name = ""
mutual_funds = False
etfs = False
stocks = False
bonds = False
alternative = False
other_investment = False
other_investment_desc = ""
personalized = False
periodic_review = False
financial_planning = False
estate_planning = False
investment_reporting = False
market_commentary = False
greater_availability = False
investment_education = False
software_tools = False
consolidation = False
other_service = False
other_service_desc = ""
recommend_rollover = False
do_not_recommend = False
current_investment_fees = ""
current_admin_expense = ""
current_other_fees = ""
current_comments = ""
rollover_investment_fees = ""
rollover_admin_expense = ""
rollover_other_fees = ""
rollover_comments = ""
other_factor_1 = ""
other_factor_2 = ""
other_factor_3 = ""
signature_date = ""

reader = PdfReader(SOURCE_PDF)
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

fields = {}

if client_name:
    fields["Client Name"] = client_name
if mutual_funds:
    fields["undefined"] = "/On"
if etfs:
    fields["undefined_2"] = "/On"
if stocks:
    fields["Stocks  Equities"] = "/On"
if bonds:
    fields["Bonds  Fixed Income"] = "/On"
if alternative:
    fields["Alternative"] = "/On"
if other_investment:
    fields["Other"] = "/On"
if other_investment_desc:
    fields["Other_2"] = other_investment_desc
if personalized:
    fields["Personalized"] = "/On"
if periodic_review:
    fields["Periodic review of any changes"] = "/On"
if financial_planning:
    fields["Financial planning"] = "/On"
if estate_planning:
    fields["undefined_4"] = "/On"
if investment_reporting:
    fields["undefined_5"] = "/On"
if market_commentary:
    fields["Market commentary and"] = "/On"
if greater_availability:
    fields["Greater availability of your"] = "/On"
if investment_education:
    fields["undefined_6"] = "/On"
if software_tools:
    fields["undefined_7"] = "/On"
if consolidation:
    fields["Consolidation"] = "/On"
if other_service:
    fields["Other 3"] = "/On"
if other_service_desc:
    fields["Other_3"] = other_service_desc
if recommend_rollover:
    fields["Check Box2"] = "/Yes"
if do_not_recommend:
    fields["Check Box3"] = "/Yes"
if current_investment_fees:
    fields["Text3"] = current_investment_fees
if current_admin_expense:
    fields["Text4"] = current_admin_expense
if current_other_fees:
    fields["Text5"] = current_other_fees
if current_comments:
    fields["Text1"] = current_comments
if rollover_investment_fees:
    fields["Text6"] = rollover_investment_fees
if rollover_admin_expense:
    fields["Text7"] = rollover_admin_expense
if rollover_other_fees:
    fields["Text8"] = rollover_other_fees
if rollover_comments:
    fields["Text2"] = rollover_comments
if other_factor_1:
    fields["any other factors relevant as to why the recommendation is in your best interest 1"] = other_factor_1
if other_factor_2:
    fields["any other factors relevant as to why the recommendation is in your best interest 2"] = other_factor_2
if other_factor_3:
    fields["any other factors relevant as to why the recommendation is in your best interest 3"] = other_factor_3
if client_name:
    fields["Name of Client"] = client_name
if signature_date:
    fields["Date"] = signature_date

page1_fields = {k: v for k, v in fields.items() if k == "Client Name"}
page2_fields = {k: v for k, v in fields.items() if k not in ["Client Name", "Name of Client", "Date", "any other factors relevant as to why the recommendation is in your best interest 1", "any other factors relevant as to why the recommendation is in your best interest 2", "any other factors relevant as to why the recommendation is in your best interest 3"]}
page3_fields = {k: v for k, v in fields.items() if k in ["Name of Client", "Date", "any other factors relevant as to why the recommendation is in your best interest 1", "any other factors relevant as to why the recommendation is in your best interest 2", "any other factors relevant as to why the recommendation is in your best interest 3"]}

if page1_fields:
    writer.update_page_form_field_values(writer.pages[0], page1_fields)
if page2_fields:
    writer.update_page_form_field_values(writer.pages[1], page2_fields)
if page3_fields:
    writer.update_page_form_field_values(writer.pages[2], page3_fields)

root = Tk()
root.withdraw()
output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
root.destroy()

if output_path:
    with open(output_path, 'wb') as output:
        writer.write(output)