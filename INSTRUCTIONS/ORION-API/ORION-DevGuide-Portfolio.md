# ORION Development Guides: PORTFOLIO

### SUB CATEGORY: Creating a New Portfolio or Household
Creating a New Portfolio or Household
Purpose: This article will outline how to create new portfolios within the Orion system.  Households are one part of a Portfolio, the other two records being a Registration and an Account.  All three records are required to create a portfolio:
Household –  (also known as Client) (Rep assignment, Address, Name, SSN for head of household).
Registration – (Account Type(ie 401K), SSN, BirthDate, Beneficiaries)
Account – (Custodian, Management Style, Fund Family, Model Assignment
Simple Use Case: A firm has a CRM or New Account Process which begins in another platform, but has the feature of creating that new portfolio in Orion as needed.
Scope and Outputs: This will allow you to create data for new entities in Orion and provide details on the required items for entity creation.   
 Process Overview:
Compose the information for the entity to be created.
Send the required data to Orion to create the new entity.
Process Steps:
GET template for creating a new Portfolio.
 GET /Portfolio/Accounts/NewPortfolio/New 
POST the required data for creating a new Portfolio.
POST /Portfolio/Accounts/NewPortfolio OR
POST /Portfolio/Accounts/NewPortfolio?generateAccountNumber={generateAccountNumber}
Here are the Required fields (noted by the *), and some of the more common fields.
CLIENT RECORD
*LastName, FirstName and Name fields must be populated. (Name is generally “firstname lastname” but not required to be. If adding to existing Household or Registration only entity ID is required.)
*StatusType Must have a value (default is recommended: “Pending Review”)
ssN_TaxID (not required, but helps with householding)
representativeId (if not filled in, it will be populated with a default rep) GET: /Portfolio/Representatives/Simple
NOTE: If using an already existing household, only the Client.Id property needs to be populated.
REGISTRATION RECORD
*LastName, FirstName and Name fields must be populated (Name is generally “firstname lastname” but not required to be. If adding to existing Household or Registration only entity ID is required.)
*TypeId (this is the account type, not required if adding to existing registration; see: GET v1/Portfolio/Registrations/Types)
DOB
ssN_TaxID
NOTE: If using an already existing registration, only the Client.Registration.Id property needs to be populated.
ACCOUNT RECORD
*FundFamilyId see: GET v1/Portfolio/FundFamilies
*CustodianId see: GET v1/Portfolio/Custodians/Simple
The following fields may be populated with defaults when calling the template GET /Portfolio/Accounts/NewPortfolio/New – If they are not you must include data.
*PayMethodId – Include the pay method see GET:/Billing/PayMethods
*FeeScheduleID Include Fee Schedule ID See GET:/Billing/Schedules
*MasterPayoutScheduleID Include payout schedule ID See GET:/Billing/MasterPayoutSchedule
aggregateModel– assigns a model to the account. see: GET v1/Trading/ModelAggs/Simple *please see notes below
CustodialAccountNumber – the custodial account number if you already have it from the custodian.
NOTE: If you know the account number, please include this upon creation under the “custodialAccountNumber”: null, of the account payload. If you do not know the account number, you can later add this data by adding an asset to an existing account and inputting the account number at that time.
This sample will create a new Household for a client named “Household Creation” with only the required fields completed. NOTE: If you are creating a new registration and account only, you can include the client id for an existing household, or both client and registration id if creating only a new account in an existing registration. Example listed below.
Code:
{
  "client": {
    "id": 0,
    "name": "Household Creation",
    "billing": {
      "billClientId": 0,
      "statusType": "Pending Review",
      "masterPayoutScheduleId": null,
      "feeScheduleID": null,
      "relatedClients": null
    },
    "recurringAdjustments": null,
    "feePayingAccounts": null,
    "tieredFeeAccounts": null,
    "householdBills": null,
    "financialPlanningFee": null,
    "portfolio": {
      "startDate": null,
      "isActive": true,
      "representativeId": 12,
      "categoryId": 1,
      "statementDeliveryMethodId": 1,
      "videoStatementDeliveryMethod": "Unassigned",
      "createdBy": null,
      "createdDate": "0001-01-01T00:00:00-06:00",
      "editedBy": null,
      "editedDate": "0001-01-01T00:00:00-06:00",
      "firstName": "Household",
      "lastName": "Creation",
      "city": null,
      "state": null,
      "isUsResident": true,
      "email": null,
      "name": "test test",
      "salutation": null,
      "lastStatementSentTo": null,
      "address1": null,
      "address2": null,
      "address3": null,
      "zip": null,
      "country": null,
      "homePhone": null,
      "homePhoneExt": null,
      "fax": null,
      "faxExt": null,
      "pager": null,
      "pagerExt": null,
      "mobilePhone": null,
      "businessPhone": null,
      "businessPhoneExt": null,
      "otherPhone": null,
      "otherPhoneExt": null,
      "workPhone": null,
      "workPhoneExt": null,
      "reportName": null,
      "company": null,
      "jobTitle": null,
      "ssN_TaxID": null,
      "gender": null,
      "advClientCategoryId": null,
      "dob": null,
      "webAddress": null,
      "importKey": null,
      "lastStatementSent": null,
      "isQualifiedInvestor": false
    },
    "householdMembers": null,
    "notes": null,
    "documents": null,
    "additionalAccounts": null,
    "suitability": null,
    "userDefinedFields": null,
    "entityOptions": null,
    "targetAllocations": null,
    "creditCard": null,
    "assetExclusions": null,
    "portfolioGroups": null,
    "appLinks": null,
    "additionalRepresentatives": null
  },
  "registration": {
    "id": 0,
    "name": "reg test",
    "portfolio": {
      "name": "reg test",
      "firstName": "reg",
      "lastName": "test",
      "typeCode": null,
      "isBIRA": false,
      "accountType": null,
      "isActive": true,
      "clientId": 0,
      "typeId": 1,
      "company": null,
      "isUsResident": true,
      "jobTitle": null,
      "ssN_TaxID": null,
      "deceasedSSN_TaxID": null,
      "dob": null,
      "gender": null,
      "createdBy": null,
      "createdDate": "0001-01-01T00:00:00-06:00",
      "editedBy": null,
      "editedDate": null,
      "dateOfDeath": null,
      "targetSpendRate": null,
      "targetDollarAmount": null,
      "targetDate": null
    },
    "contact": null,
    "notes": null,
    "beneficiaries": [],
    "suitability": {
      "netWorthIncludingResidence": null,
      "netWorthExcludingResidence": null,
      "liquidNetWorth": null,
      "investmentKnowledge": null,
      "riskExposure": null,
      "investmentExperience": null,
      "returnObjective": null,
      "investmentObjective": null,
      "timeHorizon": null,
      "stockPercent": null,
      "riskTolerance": null,
      "netWorth": null,
      "netIncome": null,
      "riskBudget": null,
      "isLifestyleOption": false,
      "reviewCompleted": null,
      "reviewCompletedDate": null
    },
    "userDefinedFields": null,
    "entityOptions": null,
    "additionalRepresentativesPercent": null
  },
  "account": {
    "id": 0,
    "name": "account test",
    "number": null,
    "billing": {
      "billAccountId": 0,
      "accountType": null,
      "fundName": null,
      "feeSchedule": "UnAssigned",
      "masterPayoutSchedule": "Blankdb",
      "payMethod": null,
      "billFrequency": "Quarterly",
      "billStyle": "Advanced",
      "acceptsList": true,
      "valuationMethod": "Period End Value",
      "fundFamilyId": 9,
      "managementStyleId": null,
      "subAdvisorId": null,
      "feeScheduleId": 4,
      "masterPayoutScheduleId": 1,
      "payMethodId": 1,
      "billStartDate": null,
      "bankName": null,
      "abaNumber": null,
      "bankAccountNumber": null,
      "nameOnAccount": null,
      "custodialAccountNumber": null,
      "isPerformanceBilled": null,
      "lastPerfBillDate": null,
      "expirationDate": null,
      "addressLine1": null,
      "addressLine2": null,
      "addressLine3": null,
      "city": null,
      "state": null,
      "zip": null,
      "includeInAggregate": true,
      "nonManagedAccountNumber": null,
      "nonManagedAccountName": null,
      "nonManagedHouseholdName": null,
      "cycleMonth": 1,
      "performanceMasterPayoutSchedule": null,
      "performanceFeeSchedule": null,
      "performanceMasterPayoutScheduleId": null,
      "performanceFeeScheduleId": null,
      "cardType": null,
      "nameOnCard": null,
      "billAccountStatus": "Ready",
      "tieredFeePriority": 0,
      "paysForAccounts": null,
      "payedByAccounts": null,
      "payeeList": null,
      "feeHierarchyItems": null,
      "creditCardNumber": null,
      "accountHistoryBillingId": null,
      "byAllAccountId": null,
      "quovoAccountId": null,
      "plaidAccountId": null,
      "akoyaAccountId": null,
      "useFeeHierarchy": false
    },
    "portfolio": {
      "clientId": 0,
      "registrationId": 0,
      "registrationName": null,
      "managementStyle": null,
      "fundFamily": null,
      "accountStartValue": null,
      "accountStartDate": null,
      "isManaged": true,
      "isActive": true,
      "isSweepAccount": true,
      "isSleeveAccount": false,
      "isSleeveCustodialAccount": false,
      "importKey": null,
      "outsideId": null,
      "managementStyleId": 24,
      "fundFamilyId": 9,
      "accountHistoryId": null,
      "modelName": null,
      "accountType": null,
      "custodian": null,
      "custodianId": 40,
      "shareClass": null,
      "shareClassId": 1,
      "subAdvisor": null,
      "subAdvisorId": null,
      "downloadSource": null,
      "downloadSourceId": null,
      "provider": null,
      "plan": null,
      "businessLine": null,
      "createdBy": null,
      "createdDate": "0001-01-01T00:00:00-06:00",
      "editedBy": null,
      "editedDate": null,
      "accountStatusId": 6,
      "accountStatusDescription": null,
      "isPositionOnlyRecon": false,
      "eclipseFirmId": null,
      "isUnfunded": false,
      "isBundled": false,
      "isExcludedFromFirmAssets": false,
      "isDefaultFundFamily": false,
      "custodialRepCode": null,
      "isOps": false,
      "lastPositionDate": null,
      "inBalance": null
    },
    "modelingInfo": {
      "modelGroupNumber": null,
      "isOriginalSMCAccount": null,
      "isTradingBlocked": false,
      "isRegistrationDoNotTrade": false,
      "tradingInstructions": null,
      "downloadSource": null,
      "createdDate": null,
      "createdBy": null,
      "editedDate": null,
      "editedBy": null,
      "isRebalance": true,
      "isOutsideModel": false,
      "minimumCashBalance": null,
      "minimumCashBalanceType": "Dollars",
      "replenishMinimumCash": false,
      "fundList": null,
      "autoRebalanceFrequency": "None",
      "autoRebalanceMonth": 1,
      "autoRebalanceDay": 1,
      "dollarModelId": null,
      "dollarModelAmount": 0,
      "expireMinCash": null,
      "expireMinCashType": null,
      "expireMinCashDate": null,
      "aggregateModel": null,
      "isSleeveAccount": false,
      "customAllocations": null
    },
    "notes": null,
    "documents": null,
    "compliance": {
      "sloas": [],
      "advCustodyTypeId": 0,
      "is13FReportable": true,
      "isAdvReportable": true,
      "isAuaReportable": false,
      "isDiscretionary": true,
      "isWrapManaged": false,
      "isWrapSponsored": false
    },
    "systematics": null,
    "accountManagers": null,
    "recurringAdjustments": null,
    "generalAccounts": null,
    "referralSchedules": null,
    "billAccountSchedules": null,
    "userDefinedFields": null,
    "entityOptions": null,
    "targetAllocations": null,
    "productEquivalents": null,
    "sma": null,
    "bondTrade": null,
    "compositeExclusions": null,
    "futureCashflows": null,
    "growthRates": null,
    "goals": null,
    "suitability": null,
    "permissibleAggregateModels": null,
    "astroTaxSchedules": null,
    "astroAccount": null,
    "taxRates": null,
    "additionalClients": null
  }
} 
Here is code sample for adding a new account to an existing Household and registration with the required fields included along with the custodial account number and model being assigned.
{
"client": {
"id": 1238
},
"registration": {
"id": 2342
},
"account": {
"id": 0,
"name": "account test",
"number": null,
"billing": {
"custodialAccountNumber": "123-4567890",
"payMethodId": 1,
"feeScheduleID": 55,
"masterPayoutScheduleId": 1
},
"portfolio": {
"clientId": 1238,
"registrationId": 2342,
"registrationName": null,
"managementStyle": null,
"fundFamily": null,
"accountStartValue": 0,
"accountStartDate": null,
"isManaged": true,
"isActive": true,
"isSweepAccount": true,
"isSleeveAccount": false,
"isSleeveCustodialAccount": false,
"importKey": null,
"outsideId": null,
"managementStyleId": null,
"fundFamilyId": 45,
"accountHistoryId": null,
"modelName": null,
"accountType": null,
"custodian": null,
"custodianId": 3,
"shareClass": null,
"shareClassId": 1,
"subAdvisor": null,
"subAdvisorId": null,
"downloadSource": null,
"downloadSourceId": null,
"provider": null,
"plan": null,
"businessLine": null,
"createdBy": null,
"createdDate": null,
"editedBy": null,
"editedDate": null,
"accountStatusId": 1,
"accountStatusDescription": null,
"isPositionOnlyRecon": false,
"eclipseFirmId": null,
"isUnfunded": false,
"isBundled": false,
"isExcludedFromFirmAssets": false,
"isDefaultFundFamily": false,
"custodialRepCode": null,
"isOps": false,
"lastPositionDate": null,
"inBalance": null
},
"modelingInfo": {
"modelGroupNumber": null,
"isOriginalSMCAccount": null,
"isTradingBlocked": false,
"isRegistrationDoNotTrade": false,
"tradingInstructions": null,
"aggregateModel": {
"id": 235
}
},
"compliance": {
"is13FReportable": true,
"isAdvReportable": true
}
Process Tips or Controls: Most common issues are not having all the required fields correctly completed.  Please be sure to update all name, firstname, lastname, typeID, FundFamilyID and custodianId fields.  If you are using an existing household or registration, you can include the client.id or registration.id for the existing entities.
When including model assignment the ID will need to be included in the “ModelingInfo” section as such.
"modelingInfo": {
"aggregateModel": {
"id": 234
}}


---


### SUB CATEGORY: Adding Transactions
This will allow you to create transactions via the API, including any offsets for applicable transaction types.  Single and Multiple transactions creation is supported.
Process Overview:
GET: /Portfolio/Tranactions/Verbose/New
               This will provide a Template for the following POST
POST:  /Portfolio/Transactions/Verbose
OR  /Portfolio/Transactions/Verbose?createOffset=true <-used to allow the API to automatically create offsets for applicable transaction types.  
Items in green are required fields, and blue are recommended.
{
    "portfolio": {
        "productId": 0,
        "productName": null,
        "ticker": null,
        "transDate": "05/28/2025",
        "transTime": "1900-01-01T16:30:40.000Z",
        "transAmount": 102.69,
        "navPrice": 102.69,
        "noUnits": 1,
        "assetId": 50020,
        "status": "Complete",
        "transactionDescription": null,
        "notes": "Testing",
        "transTypeId": 10,
        "transactionSubTypeId": null,
        "transactionSubTypeName": null,
        "contributionCodeId": null,
        "distributionCodeId": null,
        "accountId": 7068,
        "accountNumber": null,
        "managementStyle": null,
        "payee": null,
        "advisorNotes": null,
        "state": null,
        "settleDate": null,
        "tradeReferenceNumber": null,
        "transactionLinkCode": null,
        "createdBy": null,
        "createdDate": "0001-01-01T00:00:00-06:00",
        "editedBy": null,
        "editedDate": null,
        "registrationId": 0,
        "clientId": 1836,
        "typeCode": null,
        "typeSource": null,
        "signField": null,
        "eclipseOrderId": null,
        "performanceFeeBreak": false,
        "financialType": "Other"
    },
    "id": 0
}
Process Tips or Controls:
Examples for /Portfolio/Transactions/Verbose?createOffset=true ßused to create offsets for applicable transaction types.
Merge In → Because this is a new transaction not sourced from cash, no offset is needed.
Buy trade → Because this involves buying a security using cash, a cash offset will be created to reduce the cash balance accordingly.


---


### SUB CATEGORY: Creating Client Level Users
Creating Client Level Users
Purpose: This article will step through how to create Client level users via the API, as you would via the Manage Users app in Orion Connect.  This will include how to assign the Household user should be associated with.
Simple Use Case:  You would like to create new Client level users via the API.
Scope and Outputs: This is for the creation of Client level logins.  The client must have a household already created in Orion.  Please see Creating a New Portfolio or Household for instructions on creating the household. 
Process Overview: Determine the Household to assign the new user.  Update payload with details for user and household and POST newly created payload to create login and provide temp password.
Process Steps:
Add the user data to the Profiles section of the payload. In the “profiles” section, be sure to include all data except role, this will remain null for client users. 
POST payload to  Security/Users?sendEmail=false
Sample payload
{
	"profiles": [{
		"alClientId": 1350,
		"advisorName": "Orion Integration Demo",
		"entity": "Household",
		"entityName": "Dean And Elizabeth Martin",
		"loginEntityId": "Client",
		"entityId": 119,
		"isUserDefault": true,
		"isInCurrentDb": true,
		"roleId": null,
		"hideRole": true
	}],
	"password": null,
	"isSecureExchangeRecipient": false,
	"partnerAppId": null,
	"errorMessage": null,
	"id": 0,
	"userId": "annie.test.12",
	"firstName": "Dean And Elizabeth",
	"lastName": "Martin",
	"email": "bethmartin1@advisorengine.net",
	"isActive": true,
	"activeDate": null,
	"inactiveDate": null,
	"lastLogin": null,
	"lastPasswordChange": null,
	"isReset": null,
	"mobilePhone": "801-319-4052",
	"businessPhone": "4078675306",
	"businessPhoneExtension": "",
	"company": null,
	"jobTitle": null,
	"entityName": "Martin, Dean And Elizabeth"
}
Sample Response:
{
  "profiles": [
    {
      "id": 6963858,
      "loginEntityId": 4,
      "entity": "Household",
      "entityId": 119,
      "advisorName": "Orion Integration Demo",
      "entityName": "Dean Martin",
      "roleId": 5,
      "isUserDefault": true,
      "alClientId": 1350,
      "roleName": "Default Client",
      "isInCurrentDb": true
    }
  ],
  "password": "bI0wz6fddS",
  "isSecureExchangeRecipient": false,
  "partnerAppId": null,
  "errorMessage": null,
  "id": 1745614,
  "userId": "user.test.13",
  "firstName": "Dean And Elizabeth",
  "lastName": "Martin",
  "email": "test@test.net",
  "isActive": true,
  "activeDate": "2022-11-30",
  "inactiveDate": null,
  "lastLogin": null,
  "lastPasswordChange": null,
  "isReset": true,
  "mobilePhone": "800-800-0000",
  "businessPhone": "4008005006",
  "businessPhoneExtension": "",
  "company": null,
  "jobTitle": null,
  "entityName": "Martin, Dean And Elizabeth"
}
Process Tips and Controls:
Orion best practice is to use the email of the user as the userID, but not required. 
2. If sentEmail=true when submitting the request, an email will be sent to the email listed in the payload with a reset link to update the password. 
3. Optional fields are first name, job title, company, and business phone.  Mobile is not requited but is recommended for two factor authentication. 

---

### SUB CATEGORY: Updating Custom Fields (User Defined Fields)
Updating Custom Fields (AKA: User Defined Fields)
Purpose: Custom Fields can be utilized withing Portfolio Audit, custom Reports, and Queries.  They help organize and track unique identifiers for the Representative, Household, Registration, Account, and Product levels.  Below you will find steps on how to update your previously created User Defined Fields. 
Simple Use Case: You have a unique identifier that you would like to include on an Orion entity for tracking that isn’t already included elsewhere in the Orion system that needs to be updated.   
Scope and Outputs: This workflow will step through updating existing Custom Fields.  It is recommended to create the Custom Fields in the UI.  To download the Creating Custom Fields help document, click https://api.orionadvisor.com/orionconnectapp/index.html?orionSupportRedirect=%2Fs%2Farticle%2FCreating-Custom-Fields.
Process Overview: Get the existing custom field information for the entity you would like to update. Once the custom field information has been obtained, make the updates for the correlating changes and return the entire payload to process the updates. 
Process Steps:
Get the Custom Fields for the desired entity: The following example is for Client(household) level data.
GET: /portfolio/{entity}/verbose/{key}?expand=userdefinedfields ; in this instance I used GET /portfolio/clients/verbose/46?expand=userdefinedfields
Update the “value” for the custom field you would like to update. 
Return the entire payload as a PUT to the same endpoint. 
PUT: /portfolio/clients/verbose/46?expand=userdefinedfields 
{
  "id": 46,
  "name": "Papa Smurf",
  "billing": null,
  "recurringAdjustments": null,
  "feePayingAccounts": null,
  "tieredFeeAccounts": null,
  "householdBills": null,
  "financialPlanningFee": null,
  "portfolio": null,
  "householdMembers": null,
  "notes": null,
  "documents": null,
  "additionalAccounts": null,
  "suitability": null,
  "userDefinedFields": [
	{
      "userDefineDataId": 1000,
  	"value": "800009",
      "childParameter": null,
  	"entity": "Household",
  	"entityId": 46,
      "entityName": null,
      "userDefineDefinitionId": 306,
  	"name": "Outside Revenue",
  	"category": "No Category",
  	"type": "Currency",
  	"code": "5OUTSIDERE",
  	"sequence": 9,
  	"options": [],
  	"input": null,
      "securityCode": null,
  	"canEdit": false
	},
   ],
  "entityOptions": null,
  "targetAllocations": null,
  "creditCard": null,
  "assetExclusions": null,
  "portfolioGroups": null,
  "appLinks": null,
  "additionalRepresentatives": null
}
Process Tips or Controls:
Be sure to pass back all data in the payload, even for the data on the custom field that will not be changing. 
If you are updating more than one account, be sure to include the payload for each account you’re updating, and use the PUT without the key. /portfolio/{entity}/verbose/{key}?expand=userdefinedfields