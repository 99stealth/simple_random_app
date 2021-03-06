# Simple random application
[![Build Status](https://travis-ci.org/99stealth/simple_random_app.svg?branch=master)](https://travis-ci.org/99stealth/simple_random_app)

This project is created only for educational purposes. Feel free to *fork* and use it

## Before you start
Before you run deploy of the application you need to prepare the infrastructure. You can automatically deploy it using [Simple infrastructure repository](https://github.com/99stealth/simple-infrastructure "Simple Infrastructure")

:warning: Important! You can't automatically deploy this application without the AWS ECS infrastructure

## Requirements
In order to use current build and deployment process you need to have:
- GitHub account (thanks captain obvious)
- AWS account with already deployed [Simple infrastructure repository](https://github.com/99stealth/simple-infrastructure "Simple Infrastructure") CloudFormation stacks
- Dockerhub account
- Travis CI account

## Travis CI setup
Continuous integration and deployment process for current project is running on Travis CI. 
- In order to proceed with Travis CI go to https://travis-ci.org and [Sign Up](https://travis-ci.org "TravisCI") using your GitHub account
- Now go to https://travis-ci.org/account/repositories and find `simple_random_app`. Switch on checkboxes it will allow you to build the project with Travis CI
- Now go to the job and press `More options > Settings`
- Here you need to add several environment variables like
  - `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` of your who has access to `ecs*`, `cloudformation*`, `ec2*`, `cloudwatch*`
  - `AWS_DEFAULT_REGION` where you specify AWS region where your cluster is deployed
  - `dockerhub_account` and `dockerhub_password` - your dockerhub account credentials
  - `docker_repository` - your DockerHub repository where you are going to store built docker images
- Now run the build and enjoy the automation

## Rollback
When you deploy service at first time it creates the CloudWatch Event which allows to listen the for `Essential container in task exited` and sets an Alarm as a `Rollback Trigger` to current CFn stack. If the number of tasks exited tasks from updated task definition will be greater than 2 per 1 minute then rollback will be triggered.

If you want to add another alarm to Rollback Triggers you need to add Alarm which was created to `Outputs` and it should contain `Alarm` word. Deployment script will update the CFn stack with a new Rollback Trigger

## Changes in source code
It is obviously that you may want to make some changes in source code or other components. So, here are several things that you should know:
- After you make a `git push` build will be triggered
- If build is triggered from `master` branch it will also run a deploy process
- If you are changing files which are not affecting the application you may not need to run build. So, in order to make commit without build you need to run commit command with `[skip ci]` in message body, for example:
```
git add README.md
git commit -m "Commit with something important in README.md [skip ci]"
git push
```