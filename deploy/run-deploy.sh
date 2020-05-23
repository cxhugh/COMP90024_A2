#!/bin/bash

# remove the existed hosts.ini 
touch ./deploy-couchdb-clusters/inventory/hosts.ini
rm ./deploy-couchdb-clusters/inventory/hosts.ini

# setup instances 
cd ./nectarNew
. ../openrc.sh; ansible-playbook --ask-become-pass  nectar.yaml

echo "Instance have been installed, waiting 30 sec..."
sleep 30

# setup clustered couchDB 
cd ../deploy-couchdb-clusters
chmod go-wrx ./keys/*.pem
ansible-playbook -i ./inventory/hosts.ini -u ubuntu couchdb.yml