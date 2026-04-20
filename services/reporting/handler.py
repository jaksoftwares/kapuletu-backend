import json
from services.reporting.daily_summary import generate_summary

def handler(event, context):
    summary = generate_summary()
    return {
        "statusCode": 200,
        "body": json.dumps(summary)
    }
