#!/bin/bash

. ../openrc.sh; ansible-playbook -i hosts -u ubuntu --key-file=~/.ssh/db2.pem couchdb.yaml
