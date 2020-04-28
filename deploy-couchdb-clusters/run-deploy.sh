#!/bin/bash

chmod go-wrx ./keys/*.pem
. ./openrc.sh; ansible-playbook -i ./inventory/hosts.ini -u ubuntu ./deploy.yml