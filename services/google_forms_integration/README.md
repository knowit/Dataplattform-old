# Google Forms Integration

Kode.js kjører på Google App Scripts (GAS) plattformen. Den er publisert som et Google Forms tillegg (add-on), tilgjengelig på Knowit-domenet:
https://gsuite.google.com/u/1/marketplace/mydomainapps?hl=no&pann=forms_addon_widget

Google Clasp (https://github.com/google/clasp9) er brukt for å jobbe versjonskontrollere og jobbe lokalt med GAS koden. 

Appen bruker et Google Sheet for å holde styr på Google Forms som skal polles. For å legge til eller fjerne Google Forms fra Google Sheet'et, brukes Add-on'en.

Videre ligger det et trigger på GAS som går 1 gang i timen og trigger ``runAtInterval()``, som henter alle nye svar fra alle Google Form'ene registrert, og POST'er de til Main Ingest lambdaen. 