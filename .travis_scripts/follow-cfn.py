#!python

from argparse import ArgumentParser
from time import sleep
import boto3

def follow_cfn_stack(client, stack_name, try_timeout):
    cfn_stacks = client.describe_stacks(StackName=stack_name)
    while True:
        for stack in cfn_stacks["Stacks"]:
            if "IN_PROGRESS" in stack["StackStatus"] and "ROLLBACK" not in stack["StackStatus"] and "DELETE" not in stack["StackStatus"]:
                print ("Current stack status: {0}. Waiting {1} seconds".format(stack["StackStatus"], try_timeout))
                sleep(try_timeout)
            elif "COMPLETE" in stack["StackStatus"] and "DELETE" not in stack["StackStatus"]:
                print ("Current stack is {0}".format(stack["StackStatus"]))
                exit(0)
            else:
                print ("Current stack is {0}. Exit with error".format(stack["StackStatus"]))
                

def get_arguments():
    parser = ArgumentParser(description='Check stack exists')
    parser.add_argument('--stack-name', help='CFn stack name', required=True)
    parser.add_argument('--try-timeout', help='Timeouts between tries', default=15)
    return parser.parse_args()

def main():
    args = get_arguments()
    client = boto3.client('cloudformation', region_name="us-west-2")
    follow_cfn_stack(client, args.stack_name, args.try_timeout)


if __name__ == "__main__":
    main()