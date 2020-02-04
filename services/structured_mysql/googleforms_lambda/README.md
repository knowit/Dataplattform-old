# Google Forms Integration Lambda

Denne lambdaen våkner opp fra Main Ingest lambdaen via SNS. Den tar den flate datastrukturen sendt fra Google Forms og plasserer den i de tre tabellene i Aurora:
* GoogleFormsType - Her ligger alle Google Forms.
* GoogleFormsQuestionType - Her ligger alle unike spørsmålene til alle skjemaene.
* GOogleFormsAnswerType - Her ligger alle de unike svarene til alle spørsmålene i alle skjemaene. 

For at den skal fungere så må ingest.py også være deployet, med google forms filteret som sender dataen videre over SNS til denne lambdaen. I tillegg må tabellene eksisterer i databasen. create_tables.py kan brukes for å opprette tabellene. 

Ved spørsmål, kontakt Kim Duong (kim.duong@knowit.no)