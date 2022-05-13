#!/bin/bash

. ./openrc.sh; ansible-playbook -i hosts -u ubuntu --key-file=~/.ssh/ccc-group17.pem nectar.yaml

