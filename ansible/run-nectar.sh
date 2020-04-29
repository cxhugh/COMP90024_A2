#!/bin/bash

. ./group5-openrc.sh; ansible-playbook --ask-become-pass nectar.yaml
