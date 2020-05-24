#!/bin/bash

. ../openrc.sh; ansible-playbook -i ../deploy-couchdb-clusters/inventory/hosts.ini -u ubuntu analyzer_deploy.yml