 _____      _                  ___  _    _ _____ 
/  ___|    | |                / _ \| |  | /  ___|
\ `--.  ___| |_ _   _ _ __   / /_\ \ |  | \ `--. 
 `--. \/ _ \ __| | | | '_ \  |  _  | |/\| |`--. \
/\__/ /  __/ |_| |_| | |_) | | | | \  /\  /\__/ /
\____/ \___|\__|\__,_| .__/  \_| |_/\/  \/\____/ 
                     | |                         
                     |_|                         

Last ned og kjør: sudo bash setupAWS.sh

Lag en access key fra: https://console.aws.amazon.com/iam/home?#/security_credentials

Kjør: aws configure




___  ___      _         ______                               _   _____ _                   
|  \/  |     | |        | ___ \                             | | /  ___| |                  
| .  . | __ _| | _____  | |_/ /__ _ __ ___  ___  _ __   __ _| | \ `--.| |_ __ _  __ _  ___ 
| |\/| |/ _` | |/ / _ \ |  __/ _ \ '__/ __|/ _ \| '_ \ / _` | |  `--. \ __/ _` |/ _` |/ _ \
| |  | | (_| |   <  __/ | | |  __/ |  \__ \ (_) | | | | (_| | | /\__/ / || (_| | (_| |  __/
\_|  |_/\__,_|_|\_\___| \_|  \___|_|  |___/\___/|_| |_|\__,_|_| \____/ \__\__,_|\__, |\___|
                                                                                 __/ |     
                                                                                |___/      

Dette scriptet skal laste ned requirements, generere api-nøkler og starte et personlig stage for utvikleren.

1. Last ned prosjektet fra GitHub (https://github.com/knowit/Dataplattform) og lagre det på maskinen.

2. Last ned "personalStage.sh" og lagre det i mappen ".../Dataplattform/services"

3. Naviger terminalen inn til ".../Dataplattform/services" og kjør "bash personalStage.sh"
