import os
import requests
import re

def send_notification(uri, title, message):
    """
    Sends a notification based on the specified service in the URI.

    :param uri: The notification service URI (pushover, ntfy, or gotify).
    :param title: The notification title.
    :param message: The notification content.
    """

    if not uri:
        print("No notification URI provided. Skipping notification.")
        return

    # Get the notification server from the environment
    notification_server = os.getenv("NOTIFICATION_SERVER", "")

    # Parse the URI format
    match = re.match(r"(\w+)://([^@]+)@?(.*)", uri)

    if not match:
        print(f"Invalid notification URI format: {uri}")
        return

    service, user_or_token, priority = match.groups()

    # Detect the service
    if service == "pushover":
        send_pushover(notification_server, user_or_token, priority, title, message)
    elif service == "ntfy":
        send_ntfy(notification_server, user_or_token, priority, title, message)
    elif service == "gotify":
        send_gotify(notification_server, user_or_token, priority, title, message)
    else:
        print(f"Unsupported notification service: {service}")

# 🚀 Pushover Notification
def send_pushover(server, user_token, priority, title, message):
    if not server:
        server = "https://api.pushover.net/1/messages.json"

    data = {
        "token": user_token,
        "user": user_token,
        "message": message,
        "title": title,
        "priority": priority,
        "html": 1
    }
    try:
        response = requests.post(server, data=data)
        if response.status_code == 200:
            print("Pushover notification sent successfully.")
        else:
            print(f"Failed to send Pushover notification: {response.text}")
    except Exception as e:
        print(f"Error sending Pushover notification: {e}")

# 🚀 ntfy Notification
def send_ntfy(server, topic, priority, title, message):
    if not server:
        server = "https://ntfy.sh"
        print("NOTIFICATION_SERVER is not set. Using ntfy.sh by default.")

    url = f"{server}/{topic}"

    data = {
        "title": title,
        "message": message,
        "priority": priority
    }

    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("ntfy notification sent successfully.")
        else:
            print(f"Failed to send ntfy notification: {response.text}")
    except Exception as e:
        print(f"Error sending ntfy notification: {e}")

# 🚀 Gotify Notification
def send_gotify(server, token, priority, title, message):
    if not server:
        print("NOTIFICATION_SERVER is not set. Skipping Gotify notification.")
        return

    url = f"{server}/message"
    headers = {"X-Gotify-Key": token}
    data = {
        "title": title,
        "message": message,
        "priority": int(priority) if priority.isdigit() else 5
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            print("Gotify notification sent successfully.")
        else:
            print(f"Failed to send Gotify notification: {response.text}")
    except Exception as e:
        print(f"Error sending Gotify notification: {e}")
