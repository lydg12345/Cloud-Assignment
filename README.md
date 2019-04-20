# Cloud-Assignment
Group assignment

How to deploy the docker application to the CloudFormation Stack
aws cloudformation create-stack --stack-name stack --template-body file://$PWD/group7stack.yml --profile group7

aws cloudformation delete-stack --stack-name group7project --region us-west-2
