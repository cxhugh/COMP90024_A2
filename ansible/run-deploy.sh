#!/bin/bash

chmod go-wrx ./keys/*.pem
. ./group5-openrc.sh; ansible-playbook -i ./inventory/hosts.ini -u ubuntu ./deploy.yml