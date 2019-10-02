# googlesheet_airtable_integration

Dette scriptet henter data fra ett gitt google spreadsheet dokument og oppdaterer korrensponderende records i et airtable
Følgende må tilføyes i scriptet for å fungere

For airtable
- Api key
- Base ID
- Table ID

For google
- Spreadsheet ID
- Spreadsheet range (eks: "A:Q")
- credentials.json fil med google sheet api credentials må legges i mappen.

For cvpartner
- Api key

Nødvendige python biblioteker:
google-api-python-client==1.7.11
google-auth==1.6.3
google-auth-httplib2==0.0.3
google-auth-oauthlib==0.4.0
airtable-python-wrapper==0.12.0