# Google Forms Integration

Kode.js kjører på Google App Scripts (GAS) plattformen. Den er publisert som et Google Forms tillegg (add-on), tilgjengelig på Knowit-domenet: 
https://gsuite.google.com/u/1/marketplace/mydomainapps?hl=no&pann=forms_addon_widget

Google Clasp (https://github.com/google/clasp9) er brukt for å jobbe versjonskontrollere og jobbe lokalt med GAS koden.

<<<<<<< HEAD
Appen bruker et Google Sheet for å holde styr på Google Forms som skal polles. For å legge til eller fjerne Google Forms fra Google Sheet'et, brukes Add-on'en.
Google sheet'et har kolonnene fra venstre til høyre: 
* Id
* Timestamp
* QuestionsToInclude

Videre ligger det et trigger på GAS som går 1 gang i timen og trigger ``runAtInterval()``, som henter alle nye svar fra alle Google Form'ene registrert, og POST'er de til Main Ingest lambdaen. 

Nøkler til AWS og Id til Sheet'et er lagret som environment variabler inne App Scriptet. 
=======
For å kontinuerlig hente nye svar kan scriptet opprette et trigger som lytter på onSubmit. 

Nøkler til AWS og Id til Sheet'et er lagret som environment variabler inne App Scriptet.
>>>>>>> googleforms-testing

Ved spørsmål, kontakt Kim Duong (kim.duong@knowit.no)