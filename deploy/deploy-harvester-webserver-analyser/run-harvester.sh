#!/bin/bash

chmod go-wrx ../deploy-couchdb-clusters/keys/*.pem
. ../openrc.sh; ansible-playbook -i ../deploy-couchdb-clusters/inventory/hosts.ini -u ubuntu harvester_deploy.yml