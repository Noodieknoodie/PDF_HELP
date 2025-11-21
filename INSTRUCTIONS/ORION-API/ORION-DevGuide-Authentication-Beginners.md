# Storing your integration information
We have had requests to store various integration information, at different levels within orion. This allows a partner to store:
A Unique ID that links Orion Records or Users to the Partners Records or Users.
Store Authentication information, such as api tokens, secrets, or UID/PWD.
To support the different levels, or records that you may be linking, we have added support for the following levels:\
System – All of Orions Firms and Users would share the same value.
Firm – The Advisory Firm would each have their own value, this relates to an Orion Client/Database.
User – The Orion User
Profile – The Orion User + Firm. This is for the rare times when a User has access to multiple.
Client – The Orion Household Or Client record ID for the end investor.
To solve for this, we have added the following endpoints.
They support a [GET] to retrieve the value, and a [PUT] to update the value.
The object returned looks like, the IntegrationInfo Is really all you care about, it get be set to any string value (such as a token, or a json structure).
{
  "id": 1408,
  "integrationInfo": "keys",
  "level": "System"
}
Base: https://testapi.orionadvisor.com/api/v1/
{app} = This is an application code that must be assigned to you by Orion.
/Integrations/Configuration/{app}/System — Stores a value for the entire system (All Orion Firms, and Users).
/Integrations/Configuration/{app}/Firm – Stores a value for all users for a specific Firm (The firm of the user that is currently logged in ).
/Integrations/Configuration/{app}/User — Stores a value for the specific user.
/Integrations/Configuration/{app}/Profile – Stores a value for the specific profile (This is a firm/user level, as a user can have access to multiple firms).
/Integrations/Configuration/{app}/Client?clientId={orion_client_id} – Stores a value for a specific Client Id.


---


# Storing your integration information
We have had requests to store various integration information, at different levels within orion. This allows a partner to store:
A Unique ID that links Orion Records or Users to the Partners Records or Users.
Store Authentication information, such as api tokens, secrets, or UID/PWD.
To support the different levels, or records that you may be linking, we have added support for the following levels:\
System – All of Orions Firms and Users would share the same value.
Firm – The Advisory Firm would each have their own value, this relates to an Orion Client/Database.
User – The Orion User
Profile – The Orion User + Firm. This is for the rare times when a User has access to multiple.
Client – The Orion Household Or Client record ID for the end investor.
To solve for this, we have added the following endpoints.
They support a [GET] to retrieve the value, and a [PUT] to update the value.
The object returned looks like, the IntegrationInfo Is really all you care about, it get be set to any string value (such as a token, or a json structure).
{
  "id": 1408,
  "integrationInfo": "keys",
  "level": "System"
}
Base: https://testapi.orionadvisor.com/api/v1/
{app} = This is an application code that must be assigned to you by Orion.
/Integrations/Configuration/{app}/System — Stores a value for the entire system (All Orion Firms, and Users).
/Integrations/Configuration/{app}/Firm – Stores a value for all users for a specific Firm (The firm of the user that is currently logged in ).
/Integrations/Configuration/{app}/User — Stores a value for the specific user.
/Integrations/Configuration/{app}/Profile – Stores a value for the specific profile (This is a firm/user level, as a user can have access to multiple firms).
/Integrations/Configuration/{app}/Client?clientId={orion_client_id} – Stores a value for a specific Client Id.