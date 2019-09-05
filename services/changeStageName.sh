#!/bin/bash

read -p "Skriv inn stage (dev|test|prod|eget): "  inputStage
while [[ $inputStage != @(dev|test|prod|eget) ]]; do
    echo "Bruk enten dev, test, prod eller eget"
    read -p "Skriv inn stage (dev|test|prod|eget): "  inputStage
done

stageName=${inputStage,,}

#Hvis prod er inntastet, dobbelsjekker med bruker at hen vil fortsette
if [[ $stageName == prod ]]; then
    read -p "Er du sikker på valg av stage $stageName? [y/N] " confirmation
    if [ ${confirmation,,} != "y" ]; then
      echo "Avslutter..."
      exit 1
    fi
fi

#Hvis dev er innstastet, spør bruker om å bytte til personlige dev-miljø og verifiserer den inputten
if [ $stageName == "eget" ]; then
    restApiList="aws apigateway get-api-keys"
    listing=$(eval "$restApiList")
    read -p "Skriv inn dine initialer, opptil fem tegn (a-z/0-9): "  inputInitials
    stageName="dev"
    while true; do
        inputInitials=${inputInitials//[^a-zA-Z0-9_-]/_}
        inputInitials=${inputInitials//_}
        if [ "${#inputInitials}" -le 0 ]; then
            echo "Vennligst skriv inn minimum ett gyldig tegn!"
            read -p "Skriv inn dine initialer, opptil fem tegn (a-z/0-9): "  inputInitials
        elif [ "${#inputInitials}" -gt 5 ]; then
            echo "Vennligst begrens antall initaler til 5!"
            read -p "Skriv inn dine initialer, opptil fem tegn (a-z/0-9): "  inputInitials
        else
            echo "Du har skrevet inn '${inputInitials,,}' som initialer og ditt miljø vil da bli $stageName-${inputInitials,,}!"
            read -p  "Er dette riktig? [y/N] " confirmation
            if [[ $listing == *"-${inputInitials}-"* ]]; then
                echo "OBS! Disse initialene er i bruk. Hvis dette ikke er ditt miljø, vær obs på at du kan overskrive andre sitt arbeid!"
            fi
            if [ ${confirmation,,} != "y" ]; then
                echo "Du har valgt å bytte dine initialer!"
                read -p "Skriv inn dine initialer, opptil fem tegn (a-z/0-9): "  inputInitials
            else
                break
            fi
        fi
    done
    lowerCaseInitials=${inputInitials,,}
    stageName="$stageName"-"$lowerCaseInitials"
fi

for serverlessFile in $(find . -name serverless.yml); do
    echo ""
    read -p  "Vil du oppdatere stage i $serverlessFile med $stageName [y/N] " confirmation
    if [ ${confirmation,,} == "y" ]; then
      python3 changeStageName.py "$serverlessFile" "$stageName"
    fi
done




