#!/bin/bash

restApiList="aws apigateway get-api-keys"
listing=$(eval "$restApiList")

#Get initials from user to create the stage on the form "dev-{initials}"
read -p "Skriv inn dine initialer, opptil fem tegn (a-z/0-9): "  inputInitials
while true; do
    inputInitials=${inputInitials//[^a-zA-Z0-9_-]/_}
    inputInitials=${inputInitials//_}
    if [ "${#inputInitials}" -le 0 ]; then
        echo "Vennligst skriv inn minimum ett gyldig tegn!"
        read -p "Skriv inn dine initialer, opptil fem tegn (a-z/0-9): "  inputInitials
    elif [ "${#inputInitials}" -gt 5 ]; then
        echo "Vennligst begrens antall initaler til 5!"
        read -p "Skriv inn dine initialer, opptil fem tegn (a-z/0-9): "  inputInitials
    elif [[ $listing == *"-${inputInitials}-"* ]]; then
        echo "Initialene er opptatt, vennligst velg et annet sett med initialer!"
        read -p "Skriv inn dine initialer, opptil fem tegn (a-z/0-9): "  inputInitials
    else
        echo "Du har skrevet inn '${inputInitials,,}' som initialer og ditt miljø vil da bli dev-${inputInitials,,}!"
        read -p  "Er dette riktig? [Y/n]" confirmation
        if [ ${confirmation,,} == "n" ]; then
            echo "Du har valgt å bytte dine initialer!"
            read -p "Skriv inn dine initialer, opptil fem tegn (a-z/0-9): "  inputInitials
        else
            break
        fi
    fi
done
lowerCaseInitials=${inputInitials,,}
stageName="dev-$lowerCaseInitials"



#Install all required packages for the python scripts
cd ..
pip3 install -r requirements.txt



#Navigates into the "scripts"-folder to run a script in order to 
#generate api-keys, then navigate back out.
cd scripts/
printf ${stageName}'\ny\n' | python3 generate_keys.py
cd ..



#Change the default stage of all services to the new custom stage.
for serverlessFile in $(find . -name serverless.yml); do
    python3 changeStageName.py "$serverlessFile" "$stageName"
done



#Adds whitespaces to stageName to look better when printed to bash
printf -v pad %9s
stageName=$stageName$pad
stageName=${stageName:0:9}

#Creating the string that is to be printed and prints it to bash
finishedText=""
finishedText="$finishedText##############################################################\n"
finishedText="$finishedText##############################################################\n"
finishedText="$finishedText##                                                          ##\n"
finishedText="$finishedText##                        Gratulerer                        ##\n"
finishedText="$finishedText##                   Ditt miljø er: ${stageName}               ##\n"
finishedText="$finishedText##                                                          ##\n"
finishedText="$finishedText##                       Husk å kjøre                       ##\n"
finishedText="$finishedText##             sudo ./deploy_all_services ${stageName}         ##\n"
finishedText="$finishedText##                 for å deploye tjenestene                 ##\n"
finishedText="$finishedText##                                                          ##\n"
finishedText="$finishedText##############################################################\n"
finishedText="$finishedText##############################################################\n"
printf "$finishedText"