#!/bin/bash

apt update
apt -y install python3.7
apt -y install python3-pip
apt -y install awscli
pip3 install awscli --upgrade --user
apt -y install npm
npm -y install serverless -g
