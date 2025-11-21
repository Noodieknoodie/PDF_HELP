# ORION DEV GUIDE: BULK EXTRACTS

### Data Queries via API

Purpose: Orion provides customers with pre-built and custom SQL data queries that can output any data stored in the platform, in a variety of formats, and in custom layouts. These queries can be run ad-hoc through the Orion Connect Query App, scheduled to an SFTP target and/or called ad-hoc through the API.
Simple Use Case: Customer wants to export a list of households and custom fields into a CRM database connected to their Advisor platform. Customer may call the Orion API, providing the Query ID, receive back a response with the .xlsx file, which is then immediately imported into their platform.
Scope and Outputs: This workflow provides access only to queries which already exist (new ones can be built) within the Orion Connect platform. This does not provide the ability to create new queries. The data will be formatted in the same structure as the original query, but can be output to JSON, Slickgrid, simple table, .csv, .xls, or .xlsx.
Process Overview:
Identify Query (Custom Report) ID and parameters
Perform API Call with inputs for Custom Report ID and parameters
Receive response for output
Process Steps:
Locate Query ID from Orion Connect by launching Query App, navigating or filtering to the desired query, and look at the column called “Query ID”
Example: Query ID 23 = “As Of Value by Account – All Accounts”
Make GET Request to obtain query parameters. This payload is required for the next POST call to get results.
GET v1/Reporting/Custom/23
{
  "runTo": null,
  "databaseIdList": null,
  "prompts": [
    {
      "id": 22,
      "code": "@AsOfDate",
      "prompt": "Enter As of Date",
      "promptDescription": "Enter As of Date",
      "promptType": "Date",
      "defaultValue": "7/21/2021",
      "isPromptUser": true,
      "sortOrder": 1
    },
    {
      "id": 7616,
      "code": "@Status",
      "prompt": "Enter Account Status",
      "promptDescription": "0 = All Account Types, 3 = Manually Managed Only",
      "promptType": "Numeric",
      "defaultValue": "0",
      "isPromptUser": true,
      "sortOrder": 2
    },
    {
      "id": 10614,
      "code": "@fkReportCategory",
      "prompt": "Enter Reporting Category",
      "promptDescription": "Enter \"0\" for all, \"1\" for Performance, \"2\" for Activity Summary, \"4\" for Allocation, \"8\" for Portfolio Detail, \"16\" for Tax Detail.",
      "promptType": "Numeric",
      "defaultValue": "0",
      "isPromptUser": true,
      "sortOrder": 3
    }
  ],
  "source": 0,
  "id": 23,
  "scheduleIsActive": null,
  "entity": "Advisor",
  "isCustom": null,
  "isFavorite": null,
  "scheduleId": null,
  "isLandscape": false,
  "reportClass": "",
  "isInternal": false,
  "guid": "2eca3f25-87a6-4fc2-9146-3feb4394625a",
  "promptClass": "",
  "reportType": "Query",
  "userOwnerId": 2801,
  "queryType": "Custom",
  "title": "As Of Value by Account - All Accounts",
  "isNoteEnabled": false,
  "category": "OAS",
  "name": "As Of Value by Account - All Accounts",
  "description": "Returns the value for all accounts as of a specific date. Does not include zero value Accounts."
}
Make POST Request with response from previous call with required parameter values.
POST /Reporting/Custom/23/Generate
{
  "runTo": null,
  "databaseIdList": null,
  "prompts": [
    {
      "id": 22,
      "code": "@AsOfDate",
      "prompt": "Enter As of Date",
      "promptDescription": "Enter As of Date",
      "promptType": "Date",
      "defaultValue": "7/21/2021",
      "isPromptUser": true,
      "sortOrder": 1
    },
    {
      "id": 7616,
      "code": "@Status",
      "prompt": "Enter Account Status",
      "promptDescription": "0 = All Account Types, 3 = Manually Managed Only",
      "promptType": "Numeric",
      "defaultValue": "0",
      "isPromptUser": true,
      "sortOrder": 2
    },
    {
      "id": 10614,
      "code": "@fkReportCategory",
      "prompt": "Enter Reporting Category",
      "promptDescription": "Enter \"0\" for all, \"1\" for Performance, \"2\" for Activity Summary, \"4\" for Allocation, \"8\" for Portfolio Detail, \"16\" for Tax Detail.",
      "promptType": "Numeric",
      "defaultValue": "0",
      "isPromptUser": true,
      "sortOrder": 3
    }
  ],
  "source": 0,
  "id": 23,
  "scheduleIsActive": null,
  "entity": "Advisor",
  "isCustom": null,
  "isFavorite": null,
  "scheduleId": null,
  "isLandscape": false,
  "reportClass": "",
  "isInternal": false,
  "guid": "2eca3f25-87a6-4fc2-9146-3feb4394625a",
  "promptClass": "",
  "reportType": "Query",
  "userOwnerId": 2801,
  "queryType": "Custom",
  "title": "As Of Value by Account - All Accounts",
  "isNoteEnabled": false,
  "category": "OAS",
  "name": "As Of Value by Account - All Accounts",
  "description": "Returns the value for all accounts as of a specific date. Does not include zero value Accounts."
}
*You can specify with the POST request your desired format, otherwise .xlsx will be chosen by default.
Possible Formats:
/Reporting/Custom/{key:int}/Generate/xlsx
/Reporting/Custom/{key:int}/Generate/xls
/Reporting/Custom/{key:int}/Generate/csv
/Reporting/Custom/{key:int}/Generate/Table
/Reporting/Custom/{key:int}/Generate/SlickGrid
4. Collect Response as your output
Response:
[
  {
    “client ID”: 743,
    “client Name”: “Adam Smith”,
    “client Address”: “”,
    “client Address 2": “”,
    “client City”: “”,
    “client Zip”: “”,
    “client State”: ” “,
    “client Email”: “”,
    “reg ID”: 130,
    “is Qualified”: true,
    “account ID”: 307,
    “client Last Name”: “Smith”,
    “client First Name”: “Adam”,…}
…]
Process Visualization:
Process Tips or Controls:
Orion provides other methods to acquire data in real time or in a bulk flat file. If the customer’s goals are to output mass amounts of data, evaluate if the SSIS Portfolio Extract export provides a more efficient and comprehensive solution.
Data Queries have a timeout threshold of 20 minutes of run time or 1,000,000 rows of data.
As a best practice, the payload from the GET call is required to make the POST call. While some custom reports may still return without this, this is not to be an expected result and maybe be removed in a future update. Always include the payload in the POST.
The payload in the POST should not contain quotes (“) on either end of the body. This will invalidate the payload and will cause the API call to error.
If you’re getting a 201 with the report location, you’ll want to use the following to download the file: /Reporting/Custom/{key}/Run/{filename}

---

### How to Batch Pull Account and Position Balance Data

How to Batch Pull Account and Position Balance Data
Many integrations require a daily pull of account and balance data. This is to update a vendors system with all new accounts, and updated balance information from the previous days activity. These are the most common endpoints for this type of batch pull process.
Authentication. Need to get OAuth Token: http://forum.riadevelopers.com/post/authentication-oauth-8168261?highlight=oauth&trail=15
Requires client_id and client_secret.
Daily pull of Households,Accounts,Positions,Transactions.
1. Current user (use to validate which database you are currently logged into): /Authorization/User
2. Households Documentation: /Portfolio/Clients?hasValue=true
3. Accounts Documentation: /Portfolio/Accounts?hasValue=true
4. Positions Documentation: /Portfolio/Assets?hasValue=true
5. Transactions Documentation: /Portfolio/Transactions?startDate=1/18/2017
6. Tax Lots Documentation: /Reporting/Extracts/UnrealizedTaxLots
Optimization Tip: The $select parameter can be added to reduce the returned payload. If you only need an accounts Id and value, use /Portfolio/Accounts?hasValue=true&$select=Id,Value

---

### Large Data API Pulls - Best Practices

Purpose: While the API is most commonly used to get simple lists of data or all the details of an individual record, there can be use cases for extracting large amounts of data for all records for a given object. Making standard call like GET /portfolio/assets, gigabytes of data, containing millions of assets, and taking several minutes to return — assuming it doesn’t timeout!  A tough ask for any REST API.  Luckily, all our core endpoints have several options for filtering the data. 
Simple Use Case: A Customer wants to call the API daily for all assets in their entire database so that they can create a report within their own business intelligence platform of all positions held over time. They do not need all data returned from the specific endpoints and will filter down to the records and fields required.
Scope and Outputs: This article will discuss extracting assets, but the concepts can be applied to several other key data points as well.  One thing to point out though, is that these methods are focused around pulling stored data – not data that is calculated on the fly (such as cost basis, performance, asset allocation groupings, etc.).
Process Overview:
Filter down to only the records you need.
Request only the fields you need.
Split the data into chunks.
Process Steps:
With assets, the minimum filter that we require is ?hasValue=true.  This will filter down the results to only those assets with value.  You may also include things like asOfDate, editedStartDate, and/or editedEndDate.   You could also pass in a clientId, registrationId, or accountId, if you’re only needing the assets for a handful or less of these entities.  Many of these endpoints also support oData queries as well, by using the $filter parameter, which you can read about here.  So, at a minimum, after this step, your call should look like this:
GET /portfolio/assets?hasValue=true
Now that we’ve filtered down the length of the data, we’ll focus on narrowing the width of the data.  An asset object, when returned from the API in its default form, contains over 50 fields!  It’s likely that you won’t need all these fields to support the functionality you’re trying to implement, so we recommend exploring our documentation or making some sample API calls to see what is currently being returned and creating a list of the fields you do need.  Once you have this list, it’s as simple as passing them in a comma-delimited string to the $select query string parameter, like so:
GET /portfolio/assets?hasValue=true&$select=Id,AccountId,Ticker,CurrentValue
The $select parameter also comes from the oData spec, which you can read about here.  One important thing to note is that when using this feature, the field names are case-sensitive and do not have the first letter lowercased like you would see in the response objects when making the call without the $select parameter (ex. accountId becomes AccountId, currentValue becomes CurrentValue, etc).
When a data output has a related dataset, you can further specify attributes within that dataset by expanding the results and modifying your select parameter as such:
GET /Trading/ModelAggs?$expand=Details&$select=Id,Details/ModelId,Details/ModelName
If you’re regularly pulling down over 500k records, it’s time to start chunking or paging through the data. We do not recommend using the oData implementation with $skip and $top parameters. The most performant approach we’ve found for this is to start with a request for just the asset IDs, using the $select option that was discussed in Step 2, like so:
GET /portfolio/assets?hasValue=true&$select=Id
Now that you have a full list of all the asset IDs, you can split it into chunks and make requests for the full asset objects for each chunk. You’ll need to experiment with chunk sizes to find what performs best. If you’re requesting a lot of fields, use smaller chunks – just a few fields, larger chunks. For a handful of fields a good baseline is chunks of 50,000. The request for each chunk will look something like this:
POST /portfolio/assets/list/id?$select=Id,AccountId,Ticker,CurrentShares,CurrentValue
BODY [1, 2, 3, etc]  <- array containing a chunk of asset IDs
Make the chunk requests in parallel, You may optionally make the requests for each chunk in parallel, but again it’s worth experimenting to find the best performing number of parallel requests. It will likely vary depending on how many fields you’re requesting, and how many total assets will be retrieved. A good baseline to start with is 4 parallel requests.
Process Tips or Controls:
While Orion current supports $top and $skip functionality, it is formally not Orion’s best practice. This is native functionality to the REST API structure, but because it is not formally implemented into the endpoints themselves, not every endpoint will support this. As such, it is not a reliable method for filtering and should be avoided when possible. Orion may need to retire or suppress this functionality at some point for the health of the API and Database performance.
On some endpoint Orion enforces a limit which the endpoint will response with when exceeded. For example if the limit is 100,000 and you use $top=150000 – the response will be “The query specified in the URI is not valid. The limit of ‘100000’ for Top query has been exceeded.”