import requests
import os

SLACK_WEBHOOK = os.environ.get('SLACK_WEBHOOK_URL')

def escalate_to_slack(run_id, verdict, votes, memo_url):
    if not SLACK_WEBHOOK:
        print("SLACK_WEBHOOK_URL not set")
        return

    message = {
        "text": f"*Evaqa Alert*\nRun ID: {run_id}\nVerdict: {verdict}\nVotes: {votes}\nMemo: {memo_url}"
    }

    response = requests.post(SLACK_WEBHOOK, json=message)
    response.raise_for_status()
