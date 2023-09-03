from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

dynamodb = boto3.resource('dynamodb', region_name='us-east-2', endpoint_url="http://localhost:8000")

table = dynamodb.Table('Legislators')

# Search for all legislators who are female 
response = table.scan(
    FilterExpression=Attr('bio.gender').contains('F')
    )

# Sort the response
s = sorted(response['Items'], key=lambda k: (k['name'], k['code'], k['bio'], k['terms']))
print(json.dumps(s, cls=DecimalEncoder))
