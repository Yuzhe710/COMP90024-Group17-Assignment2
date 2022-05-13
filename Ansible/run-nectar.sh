#!/bin/bash

. ./openrc.sh; ansible-playbook -i inventory.ini -u ubuntu --key-file=~/.ssh/ccc-group17.pem nectar.yaml

