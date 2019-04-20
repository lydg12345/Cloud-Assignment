#!/bin/bash

aws cloudformation create-stack --stack-name stack --template-body file://$PWD/group7stack.yml --profile group7