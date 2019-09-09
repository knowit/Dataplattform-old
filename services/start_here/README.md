# start_here

Dette krever at man allerede har anskaffet seg bruker til AWS, har man ikke det kan man spørre i `#dataplattform` på Slack om hvordan man anskaffer seg dette.


## For Windows-brukere
Disse scriptene er basert på Ubuntu, og dermed trenger man `Ubuntu for Windows` for å kjøre dette.
En enkel hjelp for å installere dette finnes [her](https://tutorials.ubuntu.com/tutorial/tutorial-ubuntu-on-windows#0).


## Installere dependencies i Ubuntu
Denne mappen inneholder scripts som skal gjøre det enklere å starte med dette prosjektet.
Disse scriptene vil installere dependencies og sette opp mye av prosjektet, men ikke absolutt alt.
Det kreves en rekkefølge, da ett av scriptene krever at det andre er ferdig. Begynn med å kjøre 
```bash
sudo bash setupAWS.sh
```


## Sette opp lokal bruker i AWS
Hvis man ikke husker nøklene man skal ha fått da AWS-brukeren ble laget, kan man skaffe seg nye [her](https://console.aws.amazon.com/iam/home?#/security_credentials).
Disse nøklene skal legges inn i promptet når man kjører
```bash
aws configure
```


## Laste ned requirements og generere egen stage for utvikling
Her vil man få diverse prompt man må svare på. Dette vil sette opp en egen stage som er klar for utvikling.
Dette krever at alle tidligere punkter på denne listen er gjennomført før denne kan kjøres.
```bash
bash personalStage.sh
```


## Deploye ny stage
Hvis alt over er ferdig, så kan man deploye den nye stagen til skyen, dette gjøres ved å bruke
```bash
cd ..
./deploy_every_service.sh <stage>
```
