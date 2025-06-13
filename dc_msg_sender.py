import requests
import json

TOKENS_PATH = "tokens.json"

default_msg = {
    "content": "Default Message - Hope for World Peace! 🌍✨"
}

def dc_get_webhooks(tokens_path=TOKENS_PATH):

    with open(TOKENS_PATH, 'r') as file:
        dc_webhooks = json.load(file).get('discord_webhook_urls')

    return dc_webhooks

def dc_send_msg(msg, dc_webhooks=None):

    if dc_webhooks is None:
        dc_webhooks = dc_get_webhooks()

    if not dc_webhooks:
        print("Error: No webhooks found.")
        return

    for webhooks in dc_webhooks:
        response = requests.post(webhooks, json=msg)
        if response.status_code == 204:
            print(f"✅ Message sent successfully to {webhooks}.")
        else:
            print(f"❌ Failed to send message to {webhooks}: {response.status_code}, {response.text}")


if __name__ == "__main__":
    dc_send_msg(default_msg)