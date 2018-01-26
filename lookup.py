#!/usr/bin/env python
#
# This script is designed as wrapper to dynamically look up an AWS API Gateway
# API key and use that key to authenticate an API Gateway Request.
# The script relies on local AWS credentials configuration and receives json on
# stdin. It currently only supports endpoint queries using url query strings.
#
# Input format:
# {
#   "api_key_id": <api gateyway api key id>,
#   "endpoint": <api gateway endpoint>,
#   "query": <query string for api gateway endpoint>,
#   "region": <aws region containing desired api key>
# }
import boto3
import json
import sys
import urllib2


def get_api_key(api_key_id, region):
    # use iam credentials to lookup token for the api gateway
    client = boto3.client('apigateway', region_name=region)
    response = client.get_api_key(
        apiKey=api_key_id,
        includeValue=True
    )
    return response['value']


def main():
    if sys.version_info[0] != 2 or sys.version_info[1] < 6:
        error('This script requires Python version 2.6')

    # read stdin
    stdin = ''
    try:
        for line in sys.stdin:
            stdin = stdin + line
            data = json.loads(stdin)
    except:
        error('Error parsing stdin to JSON')

    api_key = get_api_key(data['api_key_id'], data['region'])
    opener = urllib2.build_opener()
    opener.addheaders = [('x-api-key', api_key)]

    # send http request and attempt to parse response as json
    # try:
    f = opener.open(data['endpoint'] + '?' + query_string(data['query']))
    result = f.read()
    # except:
    #     error('Error sending HTTP request')

    try:
        result = json.loads(result)
    except:
        error('Error parsing HTTP response to JSON')

    # check for errors
    if 'error' in result:
        error(result['error'])

    # concat key strings, format as hash, and print json for terraform
    try:
        print(json.dumps({
            'hosts': ','.join(result['hosts'])
        }))
    except:
        error('Error formatting results and outputting to stdout')


def query_string(query):
    p = []
    for k in query:
        p.append(k + "=" + str(query[k]))
    return '&'.join(p)


def error(str):
    sys.stderr.write(str)
    sys.exit(-1)


if __name__ == '__main__':
    main()
