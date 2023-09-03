from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal

dynamodb = boto3.resource('dynamodb', region_name='us-east-2', endpoint_url="http://localhost:8000")

table = dynamodb.Table('Legislators')

with open("data.json") as json_file:
    data = json.load(json_file, parse_float=decimal.Decimal)

    with table.batch_writer() as batch:
        for item in data:
            code = item['id']
            name = item['name']['official_full']
            bio = item['bio']
            birthday = item['bio']['birthday']
            terms = item['terms']

            print("Adding Legislator:", code, name, bio, birthday, terms)
            batch.put_item(
                Item={
                    'code': code,
                    'name': name,
                    'bio': bio,
                    'birthday' : birthday,
                    'terms': terms,
                }
            )
