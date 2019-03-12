#!python
from time import sleep
import boto3
from botocore.exceptions import ClientError
from argparse import ArgumentParser


def stack_exists(client, stack_name):
    cfn_stacks = client.list_stacks()
    for cfn_stack in cfn_stacks["StackSummaries"]:
        if cfn_stack['StackName'] == stack_name and "COMPLETE" in cfn_stack['StackStatus'] and "DELETE" not in cfn_stack['StackStatus']:
            return True
    return False

def follow_cfn_stack(client, stack_name, try_timeout):
    while True:
        cfn_stacks = client.describe_stacks(StackName=stack_name)
        for stack in cfn_stacks["Stacks"]:
            if "IN_PROGRESS" in stack["StackStatus"] and "ROLLBACK" not in stack["StackStatus"] and "DELETE" not in stack["StackStatus"]:
                print ("Current stack status: {0}. Waiting {1} seconds".format(stack["StackStatus"], try_timeout))
                sleep(try_timeout)
            elif "COMPLETE" in stack["StackStatus"] and "DELETE" not in stack["StackStatus"]:
                print ("Current stack is {0}".format(stack["StackStatus"]))
                exit(0)
            else:
                print ("Current stack is {0}. Exit with error".format(stack["StackStatus"]))
                exit(1)

def stack_operations(client, stack_name, template, try_timeout, docker_image_tag, dockerhub_repo_name, operation):
    if operation == "create":
        with open(template, 'r') as cfn_template:
            #TODO try except
            client.create_stack(StackName=stack_name,
                                TemplateBody=cfn_template.read(),
                                Parameters=[
                                  {
                                    'ParameterKey': 'dockerhubRepositoryName',
                                    'ParameterValue': dockerhub_repo_name,
                                  },
                                  {
                                    'ParameterKey': 'dockerImageTag',
                                    'ParameterValue': docker_image_tag,
                                  }
                                ]
                                )
        follow_cfn_stack(client, stack_name, try_timeout)

    elif operation == "update":
        with open(template, 'r') as cfn_template:
            try:
                return client.update_stack(StackName=stack_name,
                                           TemplateBody=cfn_template.read(),
                                           Parameters=[
                                             {
                                               'ParameterKey': 'dockerhubRepositoryName',
                                               'ParameterValue': dockerhub_repo_name,
                                             },
                                             {
                                               'ParameterKey': 'dockerImageTag',
                                               'ParameterValue': docker_image_tag,
                                             }
                                           ]
                                           )
            except ClientError as e:
                print ("[Skipping stack update] {0}".format(e))
        follow_cfn_stack(client, stack_name, try_timeout)
    else:
        print("Unknown operation {0}".format(operation))
        exit(1)

def get_arguments():
    parser = ArgumentParser(description='Check stack exists')
    parser.add_argument('--stack-name', help='CFn stack name', required=True)
    parser.add_argument('--template', help='CloudFormation template', required=True)
    parser.add_argument('--try-timeout', help='Timeouts between tries', default=15)
    parser.add_argument('--docker-image-tag', help='Docker image tag', required=True)
    parser.add_argument('--dockerhub-repo-name', help='Dockerhub repository name', required=True)
    return parser.parse_args()

def main():
    args = get_arguments()
    client = boto3.client('cloudformation')
    if stack_exists(client, args.stack_name):
        status = stack_operations(client, args.stack_name, args.template, args.try_timeout, args.docker_image_tag, args.dockerhub_repo_name, operation="update")
    else:
        status = stack_operations(client, args.stack_name, args.template, args.try_timeout, args.docker_image_tag, args.dockerhub_repo_name, operation="create")
    print (status)
        

if __name__ == "__main__":
    main()