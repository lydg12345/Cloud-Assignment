#!/bin/bash

aws cloudformation create-stack \
    --template-body file://group7stack.yml \
    --stack-name stack \
    --region us-west-2\
    --parameters ParameterKey=KeyName,ParameterValue=aws-group7project.pem\
      ParameterKey=InstanceType,ParameterValue=t2.micro
