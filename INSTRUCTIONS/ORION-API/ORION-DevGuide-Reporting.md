# ORION DEV GUIDE: REPORTING

### Benchmark Performance

Benchmark Performance
This article describes how to get performance for benchmarks. This uses the same endpoint used to get performance for any other record in the Orion system as described in the How to get performance topic.
Orion benchmarks are stored in 2 different ways.
1.) Product. These are the common indexes that we have that come directly from index sources. These are things like the S&P 500, and Russel Value 1000 indexes. They are stored in the Orion Product table just like any other equity or mutual fund, so they are just products in our system.
2.) IndexBlend. Benchmarks are created by orion users, and are made up of weighted blends of Indexes. They can also store historical changes to the underlying indexes and weightings, and also be given a “rebalance” frequency.
A list of available Product Indexes, and Index Blends can be obtained using the /portfolio/benchmarks endpoint. This will return both types of benchmarks.
https://testapi.orionadvisor.com/api/Help/Api/GET-v1-Portfolio-Benchmarks_bmType
Note that it takes a bmType, which if provided will filter the list to Benchmarks, or indexes only.
for example:
/Portfolio/Benchmarks?bmType=B returns only benchmarks, where
/Portfolio/Benchmarks?bmType=P returns indexes. (the p was used because indexes are stored as [P]roducts in our system.)
Once you have the ID, and the benchmark type (Blended Benchmark, or Index), you can call the /Reporting/Performance/Verbose endpoint.
https://testapi.orionadvisor.com/api/Help/Api/POST-v1-Reporting-Performance-Verbose
[HTTPPOST] /Reporting/Performance/Verbose
Body For getting performance for an Index Blend Benchmark:
Code:
{
"entity":"IndexBlend",
"entityIds":[1],
"groupings":[
 {"grouping":"IndexBlend"}
 ],
"startDate":"2013-01-01",
"endDate":"2013-12-31",
"returnStyle": "PortfolioSummary",
"periods":"0"
}
Body For getting performance for a benchmark (index blend):
note: 191543 is the product id for the S&P 500.
Code:
{
"entity":"Product",
"entityIds":[191543],
"groupings":[
{"grouping":"Product"}
],
"startDate":"2013-01-01",
"endDate":"2013-12-31",
"returnStyle": "PortfolioSummary",
"periods":"0"
}
If you need statistics for the benchmark, such as alpha, std. dev. etc., You can add statistics to the returnStyle property: “returnStyle”: StatisticSummary,PortfolioSummary
Further more, you can get daily return factors by adding daily to the returnStyle Property: “returnStyle”: PortfolioSummary,PortfolioDaily
---
### Getting Performance Data
Getting Performance Data
Purpose: This article provides a more streamlined and focused guide to getting performance from the Orion Reporting Scope api endpoint. See other article on Reporting Scope for a much more detailed guide to the range of solutions that can provide.
In Orion there are several levels to a portfolio. Performance can be calculated on demand for each of these levels: Household, Registration, Account, Asset, Asset Class, Asset Category and Risk Category
Simple Use Case: Firm wants to create a custom dashboard that allows a user to view Performance in a variety of ways with multiple groupings. This dashboard will call the Orion API based on the parameters entered and will retrieve the performance data for display.
Scope and Outputs: The Orion performance engine will always use the default options set for the database when calculating performance, unless overrides are specified in the POST instructions to the API.
Process Overview:
Construct the JSON set of instructions.
POST to the Orion /Reporting/Scope endpoint.
Receive the Performance results data.
Process Steps:
Using the /Reporting/Scope endpoint, you can POST a json set of instructions for what portfolio record(s) you want to use, how the performance should be returned, and how the data should be grouped.
For example, you can specify 1 or more household records and request the performance to be returned grouped by Household and Account. This will return a set of performance results for the Household, plus for every account owned by that household.
Here is an example POST body message to get performance for 3 accounts. Notice the outer calculations array only has one item, a grouping by Account that itself has 2 calculations.  So this will return Month-to-Date and Year-to-Date performance for each of the 3 accounts.
Code:
{
  "entity": "Account",
  "entityIds": [19, 20, 53],
  "asOfDate": "2020-02-29",
  "calculations": [
    {
      "id": "Accounts",
      "$type": "grouping",
      "grouping": "Account",
      "calculations": [
        {
          "id": "Month-to-Date Performance",
          "$type": "performance",
          "contextChange": {
            "reportCategoryId": 1,
            "quickDate": "MTD"
          }
        },
        {
          "id": "Year-to-Date Performance",
          "$type": "performance",
          "contextChange": {
            "reportCategoryId": 1,
            "quickDate": "YTD"
          }
        }
      ]
    }
  ]
}
Notice also that in this example every calculation item has an “id” property. This property is not used by the calculation at all. It will simply be passed through to the response to make it easier for the caller to match up the numerous calculation responses with what was requested.
Here is an example of getting performance for a Household, plus all the accounts owned by the household. Notice how each level has calculation objects included. If these are omitted the performance being requested at that level will not be calculated.
Code:
{
  "entity": "Household",
  "entityIds": [8],
  "asOfDate": "2020-02-29",
  "calculations": [
    {
      "id": "HH Month-to-Date Performance",
      "$type": "performance",
      "contextChange": {
        "reportCategoryId": 1,
        "quickDate": "MTD"
      }
    },
    {
      "id": "HH Year-to-Date Performance",
      "$type": "performance",
      "contextChange": {
        "reportCategoryId": 1,
        "quickDate": "YTD"
      }
    },
    {
      "$type": "grouping",
      "grouping": "Account",
      "calculations": [
        {
          "id": "Month-to-Date Performance",
          "$type": "performance",
          "contextChange": {
            "reportCategoryId": 1,
            "quickDate": "MTD"
          }
        },
        {
          "id": "Year-to-Date Performance",
          "$type": "performance",
          "contextChange": {
            "reportCategoryId": 1,
            "quickDate": "YTD"
          }
        }
      ]
    }
  ]
}
And that is it.
Context Change
A note on the context change object. In the examples on this page you saw reportCategoryId is always set to 1. That is because 1 is the reporting category for performance. The report category is what the numerous managed/unmanaged settings resolve into. All the reporting categories are:
1: Performance
2: Activity Summary
4: Allocation
8: PortfolioDetail
16: TaxDetail
You will notice the examples on this page set the quickDate property to either MTD or YTD. The date these use is the asOfDate the is specified on the outermost object. The best practice with that date is to set it to whatever “today” is considered to be. If you are trying to report as of the end of last quarter it should be set to the end of last quarter. The full list of quick dates can be found here.
There are additional properties if you need more control over what date range is used. You can specify a date expression string for the start and end dates to handle many scenarios. Using a date expression you can move from the specified “asOfDate” forward (+) or backward (-) by days (d), weeks (w), month (m), quarters (q) or years (y). You can also round to the start (/) or end(\) of the week, month, quarter, or year. For example if you wanted the performance for the quarter two years ago you could do this:
{
  "id": "Quarter performance for this quarter 2 years ago",
  "$type": "performance",
  "contextChange": {
    "reportCategoryId": 1,
    "dateRange": {
      "$type": "date-range",
      "startDateExpression": "-2y/q",
      "endDateExpression": "-2y\\q"
    }
  }
}
You can also specify a fixed date to date like this:
{
  "id": "Mid-January to Mid-February",
  "$type": "performance",
  "contextChange": {
    "reportCategoryId": 1,
    "dateRange": {
      "$type": "date-range",
      "startDate": "2020-01-15",
      "endDate": "2020-02-15"
    }
  }
}
If you find that the On Demand performance is not available do to lack of transactional data, the following will provide stored performance.
Stored performance is not generated day of and will likely be 1-2 days behind the on demand performance.
Stored performance should only be used if:
A) The transactional data for that time period does not exist/is unobtainable
B) Orion and the advisor have deemed the transaction data unusable
The following endpoints will return the stored performance for the level indicated using a GET:
/v1/Reporting/BI/Performance?groupEntity=Household
/v1/Reporting/BI/Performance?groupEntity=Registration
/v1/Reporting/BI/Performance?groupEntity=Account
Below is a sample of the response.  The response will be the same structure for all 3 entities (household,reg,account).  The entityId refers to the Orion ID for the record. So when running for household, it is the Orion ClientID, for Account, the Orion AccountID, and for Registration, the Orion RegistrationId.
[
  {
    "entityId": 806,
    "entityEnum": 5,
    "parentId": 0,
    "groupName": "Mariela Tellez",
    "marketValue": 36623.25,
    "day": null,
    "mtd": 0.07330073552950367,
    "qtd": 0.07330073552950367,
    "ytd": -0.11587324032871749,
    "oneYear": -0.03442694465924401,
    "threeYear": 0.06943974444330814,
    "fiveYear": null,
    "tenYear": null,
    "inception": null
  },
  {
    "entityId": 807,
    "entityEnum": 5,
    "parentId": 0,
    "groupName": "Mona Moussa",
    "marketValue": 66720,
    "day": null,
    "mtd": 0.06931253862378184,
    "qtd": 0.06931253862378184,
    "ytd": -0.09925781412126566,
    "oneYear": -0.005814441671845305,
    "threeYear": 0.08011687475632388,
    "fiveYear": null,
    "tenYear": null,
    "inception": null
  },
  {
    "entityId": 809,
    "entityEnum": 5,
    "parentId": 0,
    "groupName": "Angelica Alvarez",
    "marketValue": 1570.73,
    "day": null,
    "mtd": 0.09743793973184701,
    "qtd": 0.09743793973184701,
    "ytd": -0.10262972971428862,
    "oneYear": -0.028837316728567153,
    "threeYear": 0.08426859823536258,
    "fiveYear": null,
    "tenYear": null,
    "inception": null
  },…
---
### Household Level Portfolio View Cards
Household Level Portfolio View Cards
Purpose: This article will list out how to gather the data that is listed in Portfolio View at the household level on the Summary tab.  This will allow you to pull the same data per household for use in other applications.  Please keep in mind that this is for the raw data and you will need to determine how to display it if that is your goal.
Simple Use Case: You would like to gather Portfolio Value VS Net Amount Invest data listed for Household in the Portfolio View to display in your own Client Portal.
Scopes and Output: Data payload for each of the 6 main tiles that are shown for the Household in Portfolio View on the Summary Tab. 
Process Overview: Use the POST function for Reporting/Scope endpoint with the appropriate payload to get the data for the Portfolio View Summary tiles for the desired Household. 
Asset Category Allocation
Asset Class Allocation
Activity Summary
Portfolio Value VS Net Amount Invested
Performance VS Benchmark
Portfolio Detail
Process Steps:  POST to Reporting/Scope the Payload for the correlating tile
Asset Category Allocation
{
           	"entity": 5,
           	"entityIds": [54],
           	"asOfDate": "7/13/2021",
           	"calculations": [{
                          	"id": "AllocationDetail",
                          	"$type": "grouping",
                          	"grouping": "90",
                          	"contextChange": {
                                         	"reportCategoryId": 0
                          	},
                          	"filter": {
                                         	"$type": "filter-collection",
                                         	"filters": [{
                                                        	"$type": "currency-not-equal",
                                                        	"haystack": [null, 0],
                                                        	"context": "Self",
                                                        	"path": "Activity.Value",
                                                        	"ActivityOption": {
                                                                       	"$type": "market-value",
                                                                       	"valuationMethod": "EndingMarketValue"
                                                        	}
                                         	}],
                                         	"method": "All"
                          	},
                          	"calculations": [{
                                                        	"id": "Ticker",
                                                        	"$type": "group-info",
                                                        	"property": "ticker"
                                         	}, {
                                                        	"id": "BeginningMarketValue",
                                                        	"$type": "activity",
                                                        	"contextChange": {
                                                                       	"ActivityOption": {
                                                                                      	"$type": "market-value",
                                                                                      	"valuationMethod": "BeginningMarketValue"
                                                                       	},
                                                                       	"dateRange": {
                                                                                      	"$type": "date-range",
                                                                                      	"startDate": "1/1/2021",
                                                                                      	"endDate": "7/13/2021"
                                                                       	}
                                                        	}
                                         	}, {
                                                        	"id": "EndingMarketValue",
                                                        	"$type": "activity",
                                                        	"contextChange": {
                                                                       	"ActivityOption": {
                                                                                      	"$type": "market-value",
                                                                                      	"valuationMethod": "EndingMarketValue"
                                                                       	}
           	                                         	}
                                         	}, {
                                                        	"id": "color",
                                                        	"$type": "group-info",
                                                        	"property": "color"
                                         	},
                                         	{
                                                        	"id": "Product Type",
                                                        	"$type": "group-info",
                                                        	"entity": "Product Type",
                                                        	"property": "Name"
                                         	}, {
                                                        	"id": "AllocationDetail",
                                                        	"$type": "grouping",
                                                        	"grouping": "9",
                                                        	"contextChange": {
                                                                       	"reportCategoryId": 0
                                                        	},
                                                        	"filter": {
                                                                       	"$type": "filter-collection",
                                                                       	"filters": [{
                                                                                      	"$type": "currency-not-equal",
                                                                                      	"haystack": [null, 0],
                                                                                      	"context": "Self",
                                                                                      	"path": "Activity.Value",
                                                                                      	"ActivityOption": {
                                                                                                     	"$type": "market-value",
                                                                                                     	"valuationMethod": "EndingMarketValue"
                                                                                      	}
                                                                       	}],
                                                                       	"method": "All"
                                                        	},
                                                        	"calculations": [{
                                                                                      	"id": "Ticker",
                                                                                      	"$type": "group-info",
                                                                                      	"property": "ticker"
                                                                       	}, {
                                                                                      	"id": "BeginningMarketValue",
                                                                                      	"$type": "activity",
                                                                                      	"contextChange": {
                                                                                                     	"ActivityOption": {
                                                                                                                    	"$type": "market-value",
                                                                                                                    	"valuationMethod": "BeginningMarketValue"
                                                                                                     	},
                                                                                                     	"dateRange": {
                                                                                                                    	"$type": "date-range",
                                                                                                                    	"startDate": "1/1/2021",
                                                                                                                    	"endDate": "7/13/2021"
                                                                                                     	}
                                                                                      	}
                                                                       	}, {
                                                                                      	"id": "EndingMarketValue",
                                                                                      	"$type": "activity",
                                                                                      	"contextChange": {
                                                                                                     	"ActivityOption": {
                                                                                                                    	"$type": "market-value",
                                                                                                                    	"valuationMethod": "EndingMarketValue"
                                                                                                     	}
                                                                                      	}
                                                                       	}, {
                                                                                      	"id": "color",
                                                                                      	"$type": "group-info",
                                                                                      	"property": "color"
                                                                       	},
                                                                       	{
                                                                                      	"id": "Product Type",
                                                                                      	"$type": "group-info",
                                                                                      	"entity": "Product Type",
                                                                                      	"property": "Name"
                                                                       	}
                                                        	],
                                                        	"orderBy": [{
                                                                                      	"order": "Ascending",
                                                                                      	"path": "Group.EntityId",
                                                                                      	"globalsSynced": null
                                                                       	},
                                                                       	{
                                                                                      	"order": "Ascending",
                                                                                      	"path": "Group.Id",
                                                                                      	"globalsSynced": null
                                                                       	}
                                                        	]
                                         	}
                          	],
                          	"orderBy": [{
                                         	"order": "Ascending",
                                         	"path": "Group.SortOrder",
                                         	"globalsSynced": null
                          	}, {
                                         	"order": "Ascending",
                                         	"path": "Group.EntityId",
                                         	"globalsSynced": null
                          	}, {
                                         	"order": "Ascending",
                                         	"path": "Group.Id",
                                         	"globalsSynced": null
                          	}]
           	}],
           	"AccountManagementOverrides": []
}
Asset Class Allocation
{
           	"entity": 5,
           	"entityIds": [54],
           	"asOfDate": "7/13/2021",
           	"calculations": [{
                          	"id": "AllocationOverTime-9",
                          	"$type": "grouping",
                          	"grouping": "81",
                          	"filter": {
                                         	"$type": "filter-collection",
                                         	"filters": [{
                                                        	"$type": "currency-not-equal",
                                                        	"haystack": [null, 0],
                                                        	"context": "Self",
                                                        	"path": "Activity.Value",
                                                        	"ActivityOption": {
                                                                       	"$type": "market-value",
                                                                       	"valuationMethod": "EndingMarketValue"
                                                        	}
                                         	}],
                                         	"method": "All"
                          	},
                          	"contextChange": {
                                         	"reportCategoryId": 0,
                                         	"quickDate": "inception",
                                         	"dateRange": {
                                                        	"$type": "date-range",
                                                        	"startDate": "1/1/2021",
                                                        	"endDate": "7/13/2021"
                                         	}
                          	},
                          	"calculations": [{
                                                        	"id": "EndingMarketValue",
                                                        	"$type": "activity-series",
                                                        	"contextChange": {
                                                                       	"activityOption": {
                                                                                      	"$type": "market-value",
                                                                                      	"valuationMethod": "EndingMarketValue"
                                                                       	}
                                                        	},
                                                        	"returnStyle": {
                                                                       	"context": "Self",
                                                                       	"frequency": "Automatic",
                                                                       	"basedOn": "Calendar",
                                                                       	"cumulative": true,
                                                                       	"breakBehavior": "AllowPartialPeriods"
                                                        	}
                                         	},
                                         	{
                                                        	"id": "color",
                                                        	"$type": "group-info",
                                                        	"property": "color"
                                         	}
                          	],
                          	"orderBy": [{
                                                        	"order": "Ascending",
                                                        	"path": "Group.SortOrder",
                                                        	"globalsSynced": null
                                         	},
                                         	{
                                                        	"order": "Ascending",
                                                        	"path": "Group.EntityId",
                                                        	"globalsSynced": null
                                         	}, {
                                                        	"order": "Ascending",
                                                        	"path": "Group.Id",
                                                        	"globalsSynced": null
                                         	}
                          	]
           	}],
           	"AccountManagementOverrides": []
}
Activity Summary
{
           	"entity": 5,
           	"entityIds": [54],
           	"asOfDate": "1/31/2022",
           	"calculations": [{
                          	"id": "BeginningBondAccrual",
                          	"$type": "activity",
                          	"contextChange": {
                                         	"reportCategoryId": 0,
                                         	"ActivityOption": {
                                                        	"$type": "market-value",
                                                        	"valuationMethod": "BeginningBondAccrual",
                                                        	"inceptionValueMethod": "New Money"
                                         	},
                                         	"dateRange": {
                                                        	"$type": "date-range",
                                                        	"startDate": "2022-01-01T06:00:00.000Z",
                                                        	"endDate": "1/31/2022"
                                         	}
                          	}
           	}, {
                          	"id": "BeginningMarketValue",
                          	"$type": "activity",
                          	"contextChange": {
                          	           	"reportCategoryId": 0,
                                         	"ActivityOption": {
                                                        	"$type": "market-value",
                                                        	"valuationMethod": "BeginningMarketValue",
                                                        	"IncludeAccruedInterest": false,
                                                        	"inceptionValueMethod": "New Money"
                                         	},
                                         	"dateRange": {
                                                        	"$type": "date-range",
                                                        	"startDate": "2022-01-01T06:00:00.000Z",
                                                        	"endDate": "1/31/2022"
                                         	}
                          	}
           	}, {
                          	"id": "EndingMarketValue",
                          	"$type": "activity",
                          	"contextChange": {
                                         	"reportCategoryId": 0,
                                         	"ActivityOption": {
                                                        	"$type": "market-value",
                                                        	"valuationMethod": "EndingMarketValue",
                                                        	"IncludeAccruedInterest": false,
                                                        	"inceptionValueMethod": "New Money"
                                         	}
                          	}
           	}, {
                          	"id": "EndingBondAccrual",
                          	"$type": "activity",
                          	"contextChange": {
                                         	"reportCategoryId": 0,
                                         	"ActivityOption": {
                                                        	"$type": "market-value",
                                                        	"valuationMethod": "EndingBondAccrual",
                                                        	"inceptionValueMethod": "New Money"
                                         	}
                          	}
           	}, {
                          	"id": "Activity Summary",
                          	"$type": "grouping",
                          	"grouping": "ActivityOptions",
                          	"contextChange": {
                                         	"reportCategoryId": 0,
                                         	"dateRange": {
                                                        	"$type": "date-range",
                                                        	"startDate": "2022-01-01T06:00:00.000Z",
                                                        	"endDate": "1/31/2022"
                                         	}
                          	},
                          	"contextChanges": [{
                                         	"activityOption": {
                                                        	"$type": "activity",
                                                        	"details": [{
                                                                       	"$type": "activity",
                                                                       	"isManaged": true,
                                                                       	"flipSign": false,
                                                                       	"activityType": "16"
                                                        	}],
                                                        	"inceptionValueMethod": "New Money"
                                         	}
                          	}, {
                                         	"activityOption": {
                                                        	"$type": "activity",
                                                        	"details": [{
                                                                       	"$type": "activity",
                                                                       	"isManaged": true,
                                                                       	"flipSign": false,
                                                                       	"activityType": "32"
                                                        	}],
                                                        	"inceptionValueMethod": "New Money"
                                         	}
                          	}, {
                                         	"activityOption": {
                                                        	"$type": "activity",
                                                        	"details": [{
                                                                       	"$type": "activity",
                                                                       	"isManaged": true,
                                                                       	"flipSign": false,
                                                                       	"activityType": "512"
                                                        	}],
                                                        	"inceptionValueMethod": "New Money"
                                         	}
                          	}, {
                                         	"activityOption": {
                                                        	"$type": "activity",
                                                        	"details": [{
                                                                       	"$type": "activity",
                                                                       	"isManaged": true,
                                                                       	"flipSign": false,
                                                                       	"activityType": "1024"
                                                        	}],
                                                        	"inceptionValueMethod": "New Money"
                                         	}
                          	}],
                          	"calculations": [{
                                         	"id": "Transaction Total",
                                         	"$type": "activity",
                                         	"inceptionValueMethod": "New Money"
                          	}]
           	}],
           	"clientPerformanceInclude": "All accounts",
           	"AccountManagementOverrides": []
}
Portfolio Value VS Net Amount Invested
{
           	"entity": 5,
           	"entityIds": [54],
           	"asOfDate": "1/31/2022",
           	"calculations": [{
                          	"id": "Net Amount Invested",
                          	"$type": "activity-series",
                          	"contextChange": {
                                         	"activityOption": {
                                                        	"$type": "activity-type",
                                                        	"inceptionValueMethod": "NewMoney",
                                                        	"activityTypes": ["Contributions", "Distributions", "NetDividendsInterestGainsWithdrawn", "MergeIn", "MergeOut", "JournalIn", "JournalOut"]
                                         	},
                                         	"reportCategoryId": 0,
                                         	"quickDate": "inception",
                                         	"dateRange": null
                          	},
                          	"returnStyle": {
                                         	"context": "Self",
                                         	"frequency": "Daily",
                                         	"basedOn": "Calendar",
                                         	"cumulative": true,
                                         	"breakBehavior": "AllowPartialPeriods"
                          	}
           	}, {
                          	"id": "Ending Market Value",
                          	"$type": "activity-series",
                          	"contextChange": {
                                         	"activityOption": {
                                                        	"$type": "market-value",
                                                        	"valuationMethod": "EndingMarketValue",
                                                        	"inceptionValueMethod": "NewMoney"
                                         	},
                                         	"reportCategoryId": 0,
                                         	"quickDate": "inception",
                                         	"dateRange": null
                          	},
                          	"returnStyle": {
                                         	"context": "Self",
                                         	"frequency": "Daily",
                                         	"basedOn": "Calendar",
                                         	"cumulative": true,
                                         	"breakBehavior": "AllowPartialPeriods"
                          	}
           	}],
           	"clientPerformanceInclude": "All accounts",
           	"AccountManagementOverrides": []
}
Performance VS Benchmark
{
           	"entity": 5,
           	"entityIds": [54],
           	"asOfDate": "1/31/2022",
           	"calculations": [{
                          	"id": "Performance vs Benchmark",
                          	"$type": "grouping",
                          	"grouping": "5",
                          	"filter": {
                                         	"filters": []
                          	},
                          	"contextChange": {
                                         	"reportCategoryId": 0,
                                         	"dateRange": {
                                                        	"$type": "date-range",
                                                        	"startDate": "2022-01-01T06:00:00.000Z",
                                                        	"endDate": "1/31/2022"
                                         	}
                          	},
                          	"calculations": [{
                                         	"id": "group-performance",
                                         	"$type": "performance-series",
                                         	"returnStyle": {
                                                        	"context": "Parent",
                                                        	"frequency": "Automatic",
                                                        	"basedOn": "Calendar",
                                                        	"cumulative": true,
                                                        	"breakBehavior": "AllowPartialPeriods"
                                         	}
                          	}, {
                                         	"id": "color",
                                         	"$type": "group-info",
                                         	"property": "color"
                          	}, {
                                         	"id": "benchmarks",
                                         	"$type": "grouping",
                                         	"grouping": "Comparison",
                                         	"calculations": [{
                                                        	"id": "benchmark-performance",
                                                        	"$type": "benchmark-performance-series",
                                                        	"returnStyle": {
                                                                       	"context": "Parent",
                                                                       	"frequency": "Automatic",
                                                                       	"basedOn": "Calendar",
                                                                       	"cumulative": true,
                                                                       	"breakBehavior": "AllowPartialPeriods"
                                                        	}
                                         	}, {
                                                        	"id": "color",
                                                        	"$type": "group-info",
                                                        	"property": "color"
                                         	}]
                          	}],
                          	"orderBy": [{
                                         	"order": "Ascending",
                                         	"path": "Group.EntityId",
                                         	"globalsSynced": null
                          	}, {
                                         	"order": "Ascending",
                                         	"path": "Group.Id",
                                         	"globalsSynced": null
                          	}]
           	}],
           	"clientPerformanceInclude": "All accounts",
           	"AccountManagementOverrides": []
}
Portfolio Detail
{
           	"entity": 5,
           	"entityIds": [54],
           	"asOfDate": "1/31/2022",
           	"calculations": [{
                          	"id": "PortfolioDetailForGrouping",
                          	"$type": "grouping",
                          	"grouping": "90",
                          	"calculations": [{
                                         	"$type": "activity",
                                         	"id": "Activity",
                                         	"contextChange": {
                                                        	"reportCategoryId": 0,
                                                        	"dateRange": {
                                                                       	"$type": "date-range",
                                                                       	"startDate": "2022-01-01T06:00:00.000Z",
                                                                       	"endDate": "1/31/2022"
                                                        	}
                                         	}
                          	}, {
                                         	"id": "Group Info",
                                         	"$type": "group-info",
                                         	"property": "ticker"
                          	}, {
                                         	"id": "Product Type",
                                         	"$type": "group-info",
                                         	"entity": "Product Type",
                                         	"property": "Name"
                          	}, {
                                         	"id": "Cost Basis For Grouping",
                                         	"$type": "cost-basis",
                                         	"contextChange": {
                                                        	"reportCategoryId": 0,
                                                        	"costBasisOption": {
                                                                       	"$type": "cost-basis",
                                                                       	"realizationType": "Unrealized",
                                                                       	"includeAmortization": "false",
                                                                       	"includeDividends": "false",
                                                                       	"includeMoneyMarkets": "false",
                                                                       	"includeQualifiedAccounts": "false",
                                                                       	"includeUnknownCostBasis": "false"
                                                        	},
                                                        	"dateRange": {
                                                                       	"$type": "date-range",
                                                                       	"startDate": "2022-01-01T06:00:00.000Z",
                                                                       	"endDate": "1/31/2022"
                                                        	}
                                         	}
                          	}, {
                                         	"id": "period",
                                         	"$type": "performance",
                                         	"contextChange": {
                                                        	"reportCategoryId": 0,
                                                        	"dateRange": {
                                                                       	"$type": "date-range",
                                                                       	"startDate": "2022-01-01T06:00:00.000Z",
                                                                       	"endDate": "1/31/2022"
                                                        	}
                                         	}
                          	}, {
                                         	"id": "qtd",
                                         	"$type": "performance",
                                         	"contextChange": {
                                                        	"reportCategoryId": 0,
                                                        	"quickDate": "QTD"
                                         	}
                          	}, {
                                         	"id": "ytd",
                                         	"$type": "performance",
                                         	"contextChange": {
                                                        	"reportCategoryId": 0,
                                                        	"quickDate": "YTD"
                                         	}
                          	}, {
                                         	"id": "Estimated Income For Grouping",
                                         	"$type": "estimated-annual-income",
                                         	"contextChange": {
                                                        	"reportCategoryId": 0,
                                                        	"incomeOption": {
                                                                       	"$type": "income",
                                                                       	"modifiedDurationMarketDate": null,
                                                                       	"annualDividendRateMethod": "IDSIIndicatedAnnualDividend",
                                                                       	"prorateIncomeToMaturity": "false",
                                                                       	"showZeroYieldForZeroCouponBonds": "false",
                                                                       	"dividendDate": "ExDate"
                                                        	}
                                         	}
                          	}, {
                                         	"id": "Current Yield For Grouping",
                                         	"$type": "current-yield",
                                         	"contextChange": {
                                                        	"reportCategoryId": 0,
                                                        	"incomeOption": {
                                                                       	"$type": "income",
                                                                       	"modifiedDurationMarketDate": null,
                                                                       	"annualDividendRateMethod": "IDSIIndicatedAnnualDividend",
                                                                       	"prorateIncomeToMaturity": "false",
                                                                       	"showZeroYieldForZeroCouponBonds": "false",
                                                                       	"dividendDate": "ExDate"
                                                        	}
                                         	}
                          	}, {
                                         	"id": "PortfolioDetailForGrouping",
                                         	"$type": "grouping",
                                         	"grouping": "9",
                                         	"calculations": [{
                                                        	"$type": "activity",
                                                        	"id": "Activity",
                                                        	"contextChange": {
                                                                       	"reportCategoryId": 0,
                                                                       	"dateRange": {
                                                                                      	"$type": "date-range",
                                                                                      	"startDate": "2022-01-01T06:00:00.000Z",
                                                                                      	"endDate": "1/31/2022"
                                                                       	}
                                                        	}
                                         	}, {
                                                        	"id": "Group Info",
                                                        	"$type": "group-info",
                                                        	"property": "ticker"
                                         	}, {
                                                        	"id": "Product Type",
                                                        	"$type": "group-info",
                                                        	"entity": "Product Type",
                                                        	"property": "Name"
                                         	}, {
                                                        	"id": "Cost Basis For Grouping",
                                                        	"$type": "cost-basis",
                                                        	"contextChange": {
                                                                       	"reportCategoryId": 0,
                                                                       	"costBasisOption": {
           	                                                                       	"$type": "cost-basis",
                                                                                      	"realizationType": "Unrealized",
                                                                                      	"includeAmortization": "false",
                                                                                      	"includeDividends": "false",
                                                                                      	"includeMoneyMarkets": "false",
                                                                                      	"includeQualifiedAccounts": "false",
                                                                                      	"includeUnknownCostBasis": "false"
                                                                       	},
                                                                       	"dateRange": {
                                                                                      	"$type": "date-range",
                                                                                      	"startDate": "2022-01-01T06:00:00.000Z",
                                                                                      	"endDate": "1/31/2022"
                                                                       	}
                                                        	}
                                         	}, {
                                                        	"id": "period",
                                                        	"$type": "performance",
                                                        	"contextChange": {
                                                                       	"reportCategoryId": 0,
                                                                       	"dateRange": {
                                                                                      	"$type": "date-range",
                                                                                      	"startDate": "2022-01-01T06:00:00.000Z",
                                                                                      	"endDate": "1/31/2022"
                                                                       	}
                                                        	}
                                         	}, {
                                                        	"id": "qtd",
                                                        	"$type": "performance",
                                                        	"contextChange": {
                                                                       	"reportCategoryId": 0,
                                                                       	"quickDate": "QTD"
                                                        	}
                                         	}, {
                                                        	"id": "ytd",
                                                        	"$type": "performance",
                                                        	"contextChange": {
                                                                       	"reportCategoryId": 0,
                                                                       	"quickDate": "YTD"
                                                        	}
                                         	}, {
                                                        	"id": "Estimated Income For Grouping",
                                                        	"$type": "estimated-annual-income",
                                                        	"contextChange": {
                                                                       	"reportCategoryId": 0,
                                                                       	"incomeOption": {
                                                                                      	"$type": "income",
                                                                                      	"modifiedDurationMarketDate": null,
                                                                                      	"annualDividendRateMethod": "IDSIIndicatedAnnualDividend",
                                                                                      	"prorateIncomeToMaturity": "false",
                                                                                      	"showZeroYieldForZeroCouponBonds": "false",
                                                                                      	"dividendDate": "ExDate"
                                                                       	}
                                                        	}
                                         	}, {
                                                        	"id": "Current Yield For Grouping",
                                                        	"$type": "current-yield",
                                                        	"contextChange": {
                                                                       	"reportCategoryId": 0,
                                                                       	"incomeOption": {
                                                                                      	"$type": "income",
                                                                                      	"modifiedDurationMarketDate": null,
                                                                                      	"annualDividendRateMethod": "IDSIIndicatedAnnualDividend",
                                                                                      	"prorateIncomeToMaturity": "false",
                                                                                      	"showZeroYieldForZeroCouponBonds": "false",
                                                                                      	"dividendDate": "ExDate"
                                                                       	}
                                                        	}
                                         	}],
                                         	"orderBy": [{
                                                        	"order": "Ascending",
                                                        	"path": "Group.EntityId",
                                                        	"globalsSynced": null
                                         	}, {
                                                        	"order": "Ascending",
                                                        	"path": "Group.Id",
                                                        	"globalsSynced": null
                                         	}]
                          	}],
                          	"orderBy": [{
                                         	"order": "Ascending",
                                         	"path": "Group.SortOrder",
                                         	"globalsSynced": null
                          	}, {
                                         	"order": "Ascending",
                                         	"path": "Group.EntityId",
                                         	"globalsSynced": null
                          	}, {
                                         	"order": "Ascending",
                                         	"path": "Group.Id",
                                         	"globalsSynced": null
                          	}]
           	}],
           	"AccountManagementOverrides": [],
           	"clientPerformanceInclude": "All accounts"
}
Process Tips or Controls:
1. Household ID 54 is used in all examples.
2.  Default settings are used for all examples.  If you have edited your Portfolio View cards you may need to adjust the payload accordingly.  For instance, Update “order” to “descending” if you have made such an edit to your card. 

---

### Running a PDF Report
Running a PDF Report
Purpose: Orion has three primary types of report, standard or “canned” reports, legacy report builder reports, and report builder reports. Standard reports are pre-created by Orion for all advisors, while both legacy and new report builder reports are created by the advisors for themselves. The first two types use the same process to run through the API, but for the new report builder requests, due to the complexity of that technology, there is a different process. 
Simple Use Case: Advisor wants to generate a specific report for a Client to review or to help answer some of their questions. Rather than run this through Orion’s reporting Apps, this will instead be ran through the API into the firm’s custom Advisor Portal and associate to that Client’s report vault.
For any of our reporting options we make these reports available for their use whenever needed. If a client calls and the advisor needs to review the data for a client, they can easily pull up and run their report to get the client the information they need. 
Scope and Outputs: Running a standay/canned or legacy report will allow you to easily produce a detailed output for the requested data, but with this option we are not able to run the report to your screen, or HTML format. With the new report builder we are able to run to either option depending on need. 
Process Overview:
Standard and Legacy Report Builder Reports
Get a list of Reports and collect the Report ID
Get the report details including parameters
Choose and execute method to generate and retrieve a report
Run and wait for data
Run and poll for data when available
New Report Builder Reports
Get a list of New Report Builder Reports and collect the Report ID
Get the report details including parameters
Generate Report
Get a list of Report Inbox reports
Download Report from Report Inbox
Standard and Legacy Report Builder Process Steps:
GET a list of available reports and identify the Report ID for the report that the user wants to run.
GET v1/Reporting/Reports
GET the details about the report, including the parameters (returned in the “unstorable” collection).
GET v1/Reporting/Reports/{reportId}/Parameters
NOTE: The parameters must have the values filled in to establish what entity (client, registration, account, etc) and timeframe the report is being run for. The collection of parameters can vary from report to report. If default parameters have been set using the user interface from Orion Connect, these default parameters with automatically be used when generating the report via API.
There are two common methods for generating and receiving the report data: a) run the report and wait until the report response or b) run the report and poll for when the results are available.
Method A – Run report and wait until the report response
NOTE: While this method is simpler, a report may take a long time to generate based on the complexity and length of the report and the size of the household with the number of accounts. The timeout for the Generate API endpoint is set to 40 minutes. If your environment does not all API connections to be open that long, you should use the other method.
POST the return from step 2 with the completed parameters to v1/Reporting/Reports/{Report ID}/Generate
When this call complete, one of two things will happen:
If it was successful there will be a location header. When you GET from the location header, it will download the generated PDF.
If it was unsuccessful there will be a notification sent to the user’s report inbox with information about the problem, including an error code that can be ushered to investigate the problem. This message can be retrieved via the Report Inbox in Orion Connect or with GET v1/Reporting/ReportInbox
Method B – Run report and then poll to determine when the report is available.
POST the return from step 2 with the completed parameters, and set the “runTo” property as follows: “runTo”:
"runTo":{
"storageType":"ReportInbox",
"provider":"Self",
"combinationMethod":"None"
}
POST that object to to v1/Reporting/Reports/{Report ID}/Generate
This will return a response very quickly and include a location header that can be used to poll the status: GET v1/Reporting/Reports/{Report ID}/Generate/{guid}/Status
When running a single report that endpoint will initially return:
{
     "status": "Pending Generation",
     "reports": [],
     "totalReports": 1
}
When the report is complete it will change to be similar to:
{
     "status": "Generated",
     "reports": [
     {
          "runFor": {
               "entityId": {entityId},
               "entity": {entityLevel}
          },
          "status": "Generated",
          "location": ".../v1/Reporting/ReportInbox/{inboxId}/Download"
     }
     ],
     "totalReports": 1
}
The location property in the report object can be then used to GET the pdf. Reports run to the user’s report inbox will be available for 4 days.
New Report Builder Process Steps:
GET a list of available reports and identify the Report ID for the report that the user wants to run.
GET v1/Reporting/Envision/Reports
[
  {
    "id": "00000000-0000-0000-0000-000000000000",
    "name": "string",
    "description": "string",
    "versionOfReportId": "00000000-0000-0000-0000-000000000000",
    "canEdit": true,
    "canDelete": true,
    "auditedBy": "string",
    "auditedDate": "2020-11-18T22:17:37.693Z",
    "createdBy": "string",
    "createdDate": "2020-11-18T22:17:37.693Z"
  }
]
Get the report details including parameters
GET v1/Reportring/Reports/{reportId}/Parameters
NOTE: The parameters must have the values filled in to establish what entity (client, registration, account, etc) and timeframe the report is being run for. The collection of parameters can vary from report to report. If default parameters have been set using the user interface from Orion Connect, these default parameters with automatically be used when generating the report via API.
{	
    "id": "00000000-0000-0000-0000-000000000000",	
    "requiredOptions": [{	
            "id": "entity",	
            "$type": "select-entity",	
            "entity": "Household",	
            "options": ["Household", "Registration", "Account"],	
            "optionId": null,	
            "prompt": "Always"	
        }, {	
            "id": "daterange 0",	
            "$type": "daterange",	
            "start": {	
                "date": "2020-11-01",	
                "expression": "/m",	
                "dateSource": "Dynamic"	
            },	
            "end": {	
                "date": "2020-11-18",	
                "expression": "0d",	
                "dateSource": "Dynamic"	
            },	
            "name": "Period",	
            "dataMustExistOnRangeStartDate": false,	
            "dataMustExistOnRangeEndDate": false,	
            "allowStartDateAdjustment": true,	
            "startDateMethod": "Inception",	
            "optionId": 0,	
            "prompt": "Always"	
        }	
    ],	
    "additionalOptions": null,	
    "deliveryOptions": [{	
            "id": "delivery-method",	
            "$type": "delivery-method",	
            "options": [{	
                    "storageType": "DirectDownload",	
                    "displayName": "Direct Download",	
                    "provider": null	
                }, {	
                    "storageType": "ReportInbox",	
                    "displayName": "Report Inbox: currentusername",	
                    "provider": "0"	
                }, {	
                    "storageType": "ReportInbox",	
                    "displayName": "Report Inbox: Selected Inbox",	
                    "provider": "3"	
                }	
            ],	
            "storageType": "DirectDownload",	
            "provider": null,	
            "folderPath": null,	
            "userIdList": null,	
            "reportFormat": "Html",	
            "combinationMethod": "Aggregate",	
            "archiveReport": false,	
            "optionId": null	
        }	
    ],	
    "hasAdditionalOptions": true,	
    "reportName": "Asset Category",	
    "reportDescription": "Report Description",	
    "parentCategory": "Portfolio",	
    "category": "Custom Reports",	
    "runAssignedVersion": false	
}	
POST the updated parameters to the generate endpoint. Make sure to add the entity IDs to the entity option and update the start and end date.
POST v1/Reporting/Reports/{Report ID}/Generate
{
    "id": "00000000-0000-0000-0000-000000000000",
    "requiredOptions": [{
            "id": "entity",
            "$type": "select-entity",
            "entity": "Household",
            "options": ["Household", "Registration", "Account"],
            "optionId": null,
            "prompt": "Always",
            "entityIds": [11111]
        }, {
            "id": "daterange 0",
            "$type": "daterange",
            "start": {
                "date": "1/1/2020",
                "expression": "/m",
                "dateSource": "Static"
            },
            "end": {
                "date": "12/31/2020",
                "expression": "0d",
                "dateSource": "Static"
            },
            "name": "Period",
            "dataMustExistOnRangeStartDate": false,
            "dataMustExistOnRangeEndDate": false,
            "allowStartDateAdjustment": true,
            "startDateMethod": "Inception",
            "optionId": 0,
            "prompt": "Always"
        }
    ],
    "additionalOptions": null,
    "deliveryOptions": [{
            "id": "delivery-method",
            "$type": "delivery-method",
            "options": [{
                    "storageType": "DirectDownload",
                    "displayName": "Direct Download",
                    "provider": null
                }, {
                    "storageType": "ReportInbox",
                    "displayName": "Report Inbox: currentusername",
                    "provider": "0"
                }, {
                    "storageType": "ReportInbox",
                    "displayName": "Report Inbox: Selected Inbox",
                    "provider": "3"
                }
            ],
            "storageType": "DirectDownload",
            "provider": null,
            "folderPath": null,
            "userIdList": null,
            "reportFormat": "Html",
            "combinationMethod": "Aggregate",
            "archiveReport": false,
            "optionId": null
        }
    ],
    "hasAdditionalOptions": true,
    "reportName": "Asset Category",
    "reportDescription": "Report Description",
    "parentCategory": "Portfolio",
    "category": "Custom Reports",
    "runAssignedVersion": false
}
Get a list of reports in the user’s report inbox.
GET v1/Reporting/ReportInbox
[
  {
    "id": 0,
    "openWith": "string",
    "fileName": "string",
    "createdDate": "2020-11-23T17:35:15.103Z",
    "createdBy": "string",
    "editedBy": "string",
    "editedDate": "2020-11-23T17:35:15.103Z",
    "description": "string"
  }
]
Download report from user’s report inbox by specifying the Report ID from the previous request
GET v1/Reporting/ReportInbox/{reportInboxID}/Download

---

### Unmanaged Assets, Products, and Accounts

Unmanaged Assets, Products, and Accounts
There is a very powerful but often confusing feature in the reporting system called Unmanaged. This feature is often thought of as a way to mark an asset, product, or account as being excluded from reporting and though that is often the case, it is far from the whole story.
When dealing with the Unmanaged feature it’s not about “Is this asset managed or unmanaged?” but rather “Is this asset managed or unmanaged for a specific reporting category?”. Currently we support five report categories:
Performance (1)
Activity Summary (2)
Allocation (4)
Portfolio Detail (8)
Tax Detail (16)
A specific asset, product, or account can be marked as managed in some of these categories and unmanaged in the rest. Generally speaking, unmanaged means you want to exclude it from normal reporting but in RB3 and its derivative systems you can pick any report category to report on so unmanaged doesn’t really mean it’s excluded just put into a different bucket. In RB3 and its derivative systems you have the following options for report category:
All (0) – show everything without looking at the managed/unmanaged settings
Managed Performance (1) – only what’s managed for Performance
Managed Activity Summary (2) – only what’s managed for Activity Summary
Managed Allocation (4) – only what’s managed for Allocation
Managed Portfolio Detail (8) – only what’s managed for Portfolio Detail
Managed Tax Detail (16) – only what’s managed for Tax Detail
Unmanaged Performance (-1) – only what’s unmanaged for Performance
Unmanaged Activity Summary (-2) – only what’s unmanaged for Activity Summary
Unmanaged Allocation (-4) – only what’s unmanaged for Allocation
Unmanaged Portfolio Detail (-8) – only what’s unmanaged for Portfolio Detail
Unmanaged Tax Detail (-16) – only what’s unmanaged for Tax Detail
How to set the option?
There are two specific settings that determine which report categories a specific asset is managed for.
First we need to determine if the asset is even considered to be unmanaged. If the asset is marked as unmanaged, its product or account are marked as unmanaged then the asset in question is considered to be unmanaged.
When an asset is considered to be unmanaged the system will then look at the entity option 
Unmanaged assets inclusion
 to determine which report category(s) the asset is managed / unmanaged for. The value is stored in a bitwise fashion. So if the setting says include in Performance (1) and Allocation (4) the stored value would be 5. This uses standard entity option inheritance. It will first look for a value on the asset, then the product, then the account, then the database. NOTE: this order can change database to database. Which ever value it finds first is the value that will be used. The purpose of this is to partially include the unmanaged asset in some calculations but exclude it from others (ex: exclude from performance but include in activity value).
NOTE: It is possible for this setting to make an asset that is considered to be unmanaged be marked as included in all report categories which would make it effectively managed.