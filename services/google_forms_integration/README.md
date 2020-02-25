# Google Forms Integration

Kode.js kjører på Google App Scripts (GAS) plattformen. Den er publisert som et Google Forms tillegg (add-on), tilgjengelig på Knowit-domenet: 
https://gsuite.google.com/u/1/marketplace/mydomainapps?hl=no&pann=forms_addon_widget

Google Clasp (https://github.com/google/clasp9) er brukt for å jobbe versjonskontrollere og jobbe lokalt med GAS koden.

For å kontinuerlig hente nye svar kan scriptet opprette et trigger som lytter på onSubmit. 

Nøkler til AWS og Id til Sheet'et er lagret som environment variabler inne App Scriptet.

Ved spørsmål, kontakt Kim Duong (kim.duong@knowit.no)