# Simple random application
[![Build Status](https://travis-ci.org/99stealth/simple_random_app.svg?branch=master)](https://travis-ci.org/99stealth/simple_random_app)

This project is created only for educational purposes. Feel free to fork and use it

## Before you start
Before you run deploy of the application you need to prepare the infrastructure. You can automatically deploy it using [Simple infrastructure repository](https://github.com/99stealth/simple-infrastructure "Simple Infrastructure")

:warning: Pay attention! You can't automatically deploy this application without the AWS ECS infrastructure

## Requirements
In order to use current build and deployment process you need to have:
* GitHub account (thanks captain obvious)
* AWS account with already deployed [Simple infrastructure repository](https://github.com/99stealth/simple-infrastructure "Simple Infrastructure") CloudFormation stacks
* Dockerhub account
* Travis CI account

## Travis CI setup
Continuous integration and deployment process for current project is running on Travis CI. 
* In order to proceed with Travis CI go to https://travis-ci.org and [Sign Up](https://travis-ci.org "TravisCI") using your GitHub account
* Now go to https://travis-ci.org/account/repositories and find `simple_random_app` and `simple_infrastructure`. Switch on checkboxes it will allow you to build the project with Travis CI
* Now go to the job and press `More options > Settings`
* Here you need to add several environment variables like
  * `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` of your who has access to `ecs*`, `cloudformation*` `ec2*`
  * `AWS_DEFAULT_REGION` where you specify AWS region where your cluster is deployed
  * `dockerhub_account` and `dockerhub_password` - your dockerhub account credentials
  * `docker_repository` - your DockerHub repository where you are going to store built docker images
* Now run the build and enjoy the automation
