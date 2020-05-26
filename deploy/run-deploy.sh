#!/bin/bash

#Project: COMP90024--2020S1--Assignment2--Alcohol Tweets and Australian Cities Analytics on the Cloud
#Purpose:  to find out the correlations between alcohol-related tweets and demographic 
#         and behavioural characteristics in Australia cities.
#Team: group05-- Ruiqi Zhu (939162), Zhengyang Li (952972), Jianxin Xu (1014840), Qiuxia YIN (1017231), Fang Qu (1070888)


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

# install harvester, webserver, analyser
cd ../deploy-harvester-webserver-analyser
chmod go-wrx ./keys/*.pem
ansible-playbook -i ../deploy-couchdb-clusters/inventory/hosts.ini -u ubuntu harvester_deploy.yml
ansible-playbook -i ../deploy-couchdb-clusters/inventory/hosts.ini -u ubuntu webserver_deploy.yml
ansible-playbook -i ../deploy-couchdb-clusters/inventory/hosts.ini -u ubuntu analyzer_deploy.yml
