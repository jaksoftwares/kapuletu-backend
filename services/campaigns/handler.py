import json
from services.campaigns.service import create_campaign, list_campaigns

def handler(event, context):
    method = event.get("httpMethod")
    if method == "POST":
        body = json.loads(event.get("body", "{}"))
        return {"statusCode": 201, "body": json.dumps(create_campaign(body))}
    return {"statusCode": 200, "body": json.dumps(list_campaigns())}
