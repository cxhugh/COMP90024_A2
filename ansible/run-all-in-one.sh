#!/usr/bin/env bash

. ./group05-openrc.sh; ansible-playbook -i hosts --ask-become-pass all-in-one.yaml