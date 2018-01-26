## api-gateway-wrapper
This script is designed as wrapper to dynamically look up an AWS API Gateway
API key and use that key to authenticate an API Gateway Request.
The script relies on local AWS credentials configuration and receives json on
stdin. It currently only supports endpoint queries using url query strings.

## Input format:
```
  {
   "api_key_id": <api gateyway api key id>,
   "endpoint": <api gateway endpoint>,
   "query": <query string for api gateway endpoint>,
   "region": <aws region containing desired api key>
  }
  ```
