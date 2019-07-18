#!/bin/bash

# This list is sorted in the way we need to deploy the services.
export services=("dynamodb/" "common_layers/" "ingest/" "fetch/" "events_slack_app/" "poller/")

if [ "$1" != "" ]; then
    if [ "$2" = "remove" ]; then
        for (( idx=${#services[@]}-1 ; idx>=0 ; idx-- )) ; do
            cd "${services[idx]}"
            echo ''
            echo 'Removing' "${services[idx]}"
            echo ''
            sls remove --stage $1
            cd ..
        done
    else
        echo 'Deploying' $1 'stage.'
        for service in ${services[@]}; do 
            cd $service
            echo ''
            echo 'Deploying' $service
            echo ''
            sls deploy --stage $1
            exit_status=$?
            cd ..
            if [ $exit_status -ne 0 ]; then
                echo "ERROR! $service FAILED. Stopping the rest of the deployment scripts."
                exit $exit_status
            fi
        done 
    fi
else
    echo 'You need to specify a stage. (prod, dev, test).'
    echo 'Example: `./deploy_every_service.sh test`'
    echo 'Or if you want to remove all the services for a stage: `./deploy_every_service.sh test remove`'
fi
