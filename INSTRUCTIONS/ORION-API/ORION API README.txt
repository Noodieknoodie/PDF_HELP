# GOAL: Build a ORION mcp server for personal use within our firm to allow for Claude AI models to go under the hood and perform Orion Tasks with my oversight. There are specific tasks that will be focused on.

# WHAT IS AN MCP SERVER:  In the context of controlling Orion (the wealth management platform by Orion Advisor Solutions), an MCP server acts as a standardized integration layer that connects AI agents or conversational interfaces to Orion's REST API endpoints, enabling intelligent, natural-language-driven automation and data retrieval across the platform's financial planning, portfolio management, and reporting functions. Because Orion is API-first with every platform function exposed through REST endpoints, the MCP server translates high-level user requests or AI-generated commands into precise API calls—handling authentication, request formatting, response parsing, and error management—while maintaining security and context across multi-step workflows. This architecture allows wealth management professionals to interact with Orion using conversational AI tools (like Claude Desktop or custom agents) to query client data, generate reports, execute portfolio operations, or automate routine tasks without manually constructing API requests, effectively turning the entire Orion platform into an AI-accessible toolkit.​

# PROJECT SPECIFIC DETAILS:

* The MCP server will center on Portfolio and Reporting functions, with full access to all related data, including households, clients, accounts, registrations, holdings, transactions, documents, suitability, and raw performance/activity/cost-basis data.
* It will support complete read/write operations, allowing the AI to create, update, and retrieve Orion records across all supported portfolio entities.
* Reporting capabilities will be fully enabled, covering standard reports, custom Report Builder reports, PDF generation, and all data-level reporting queries.
* Trading functionality will not be included.
* Authentication will use API key credentials.
* The system will handle workflows such as onboarding households/accounts, generating client-facing reports, and managing all portfolio data interactions.
* Full internal access to sensitive data is permitted.
* AI is allowed to modify Orion data without restrictions across the enabled feature set.


# HOW TO: To build a functional MCP server for Orion, you need to establish the core infrastructure that bridges AI agents with Orion's REST API endpoints, ensuring authentication, tool definition, and deployment are properly configured. This involves creating the server application itself, defining how each Orion API endpoint maps to callable tools, implementing secure credential management, and documenting the complete integration so both developers and AI clients understand available capabilities.
Core Build Requirements:
1. MCP Server Application Code – Python or TypeScript server implementation using MCP SDK (FastMCP, @modelcontextprotocol/sdk) with transport layer (STDIO or HTTP/SSE) configured
2. Orion API Integration Layer – Authentication handler (OAuth 2.0 or API key), REST endpoint wrapper functions, request/response parsing, and error handling for all Orion platform operations
3. Tool Definitions & Schemas – Type-safe function signatures with docstrings defining each available operation (client queries, portfolio actions, report generation), input parameters, and return types for Claude/AI client consumption
4. Configuration & Secrets Management – Environment variables or secure vault integration for Orion API credentials, base URLs, rate limiting, and deployment-specific settings
5. Documentation & Testing Suite – Comprehensive API mapping documentation, usage examples for common workflows, integration tests validating each Orion endpoint, and deployment instructions for workstation or managed infrastructure
# Developers Getting Started Guide for the OrionApi [https://developers.orionadvisor.com/quick-start/#base-endpoints]
Building an integration with the Orion Platform.  Well, you have made an excellent choice.  You have the back-end of the premier portfolio accounting system at your http fingertips!  
API Overview
The OrionApi is a fully functional api for the Orion Portfolio Accounting System.  The API provides functionality for:
Portfolio
Retrieve, Update, and Create Portfolio records, and associated data.  This includes Households, Registrations, Financial Account Records, Assets, transactions as well as Documents, Notes, Suitability, and all the other related portfolio information.
Trading
Retrieve, Update, and Create Models, assign models to accounts. Use this domain to generate trades using all the Orion trading applications such as rebalance, trade to target percent, quick trade, excel uploads, global ticker swap and more. The trade orders can be retrieved, and submitted through custodial files, or real time FIX trade connections.
Billing
Retrieve, Update, and Create Billing information such as Fee schedules, payout schedules, adjustments, account billing instructions, related billing households.  Also get generated bill information such as Receivables, payables, and invoices.
Reporting
Ability to run Orion’s standard reports, as well as reports that have been created using Report Builder.  These reports can be run to PDF, and downloaded, saved to Orions report inbox, or saved to Cloud Storage such as DropBox, and BOX.NET.  Report data can also be queried such as tax cost basis, performance, Values, and Activity.
Orion Connect
Orion Connect allows a calling application to launch the Orion UI.  For example, if you want to launch the Orion Household Overview for a specific household from your own application, this can be done by using the Api Token.  You can also embed Orion Connect UI components within iFrames in web applications.
Test Orion Credentials
Orion credentials are required for accessing the Orion API.  These credentials are available upon request.  Please contact us to request access.
BASE API Endpoints
Base api endpoint is the base url required to make all api calls.  These base urls is what should be stored in a configuration file or table so they can be easily changed between test and production environments, or if a new version of the api is deployed (v2).
Test:
https://testapi.orionadvisor.com/api/v1
Production:
https://api.orionadvisor.com/api/v1
This is an example of launching the Orion Connect Household Overview page in a browser.
Code:
string url = OrionApi.OrionConnectLinks.HouseholdOverview( Entity.Client, clientId );
 
Process.Start(url);
This is an example for creating a new client (household) record.
Code:
// fill out the client verbose properties, and save changes.
_clientVerbose.portfolio.representativeId = (int)cboRep.SelectedValue;
_clientVerbose.portfolio.firstName = txtCientFName.Text;
_clientVerbose.portfolio.lastName = txtClientLName.Text;
_clientVerbose.portfolio.name = txtClientFullName.Text;
 
_clientVerbose.portfolio.address1 = txtClientAddr1.Text;
_clientVerbose.portfolio.address2 = txtClientAddr2.Text;
_clientVerbose.portfolio.city = txtClientCity.Text;
_clientVerbose.portfolio.state = txtClientState.Text;
_clientVerbose.portfolio.zip = txtClientZip.Text;
 
_clientVerbose = OrionApi.Portfolio.ClientSave( _clientVerbose );
---