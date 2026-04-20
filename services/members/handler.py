import json
from services.members.service import create_member, list_members

def handler(event, context):
    method = event.get("httpMethod")
    if method == "POST":
        body = json.loads(event.get("body", "{}"))
        return {"statusCode": 201, "body": json.dumps(create_member(body))}
    return {"statusCode": 200, "body": json.dumps(list_members())}
