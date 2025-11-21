# ORION DEV GUIDE: Searching Via the API

Purpose: While the API provides several ways to query an entire list of a specific entity type, often being able search for a specific client, account, or even report can help narrow the records to what you are looking for, filtering down the results. Orion provides several search endpoints to help with this need.
Simple Use Case: User would like to search for all clients, registrations, and accounts where the name contains “Paul” and have the IDs returned.
Scope and Outputs: The search endpoints specifically look at the name field for each entity and by default perform a contain function on the text input. This allows you to search for “Jo” and the response would return names such as “John”, “Joseph”, “Joan”, and “Amy Jo”. Many of the search endpoints are in Orion’s /Simple format with the response contains only basic information such as the entity ID, name, and a few key fields of data.
Append ?search= to the end of the Best practice is to use an ?isActive=true filter to remove inactive entities and to make the response manageable for a user to refine their search use an ?top=10 or ?top=20 filter to return only the top 10 or 20 results. Using the filter ?useContain=false will override the default and require an exact match on the results.
Commonly used search endpoints:
Clients or Households:  /Portfolio/Clients/Simple/Search
Client Search by Last Name: /Portfolio/Clients/Simple/Search/LastName
Portfolio Groups:  /Portfolio/PortfolioGroups/Search
Registrations:  /Portfolio/Registrations/Simple/Search
Accounts:  /Portfolio/Accounts/Simple/Search
Assets:  /Portfolio/Assets/Simple/Search
Models: /Trading/Models/Search/
Products (Securities): /Portfolio/Products/Search
Reports:  /Reporting/Reports/Simple/Search
Data Queries:  /Reporting/Custom/Simple/Search
Example of a complete URL: /Portfolio/Clients/Simple/Search?search=John%20Clark&top=24&useContain=false
Process Tips or Controls:
The Account search endpoint has a special parameter ?userDirect=true which limits the account number search to the account code field on our assets. This speeds up the search by only looking at where Orion stores the account number from the custodial files. This ignores outsideId, SecondaryAcctCode, and the billing Custodial Account Number, but if 0 matches are found it will search the registration and client name fields.