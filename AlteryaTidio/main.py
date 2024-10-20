import argparse
import requests
import json

# Replace with your Tidio API endpoint
TIDIO_API_URL = 'wss://socket.tidio.co/socket.io/?ppk=hdikhrhpbm1frocyeuro1aplei6xxdvz&device=desktop&cmv=2_0&EIO=4&transport=websocket'

VISITOR_REGISTER_FORMAT = [
    "visitorRegister",
    {
        "id": "457378265e7b4df9a572626386b7a2cd",
        "originalVisitorId": "457378265e7b4df9a572626386b7a2cd",
        "distinct_id": None,
        "country": None,
        "name": "yenav86202@avzong.com",
        "city": None,
        "browser_session_id": "",
        "created": 1729422902,
        "email": "yenav86202@avzong.com",
        "project_public_key": "hdikhrhpbm1frocyeuro1aplei6xxdvz",
        "phone": "",
        "ip": None,
        "lang": "en-us",
        "browser": "Chrome",
        "browser_version": 129,
        "url": "",
        "refer": "",
        "os_name": "Windows",
        "os_version": "",
        "screen_width": 1536,
        "screen_height": 960,
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "timezone": "Asia/Jerusalem",
        "mobile": False,
        "is_chat_on_site": False,
        "wd": "t",
        "emailConsent": {
            "value": "unsubscribed",
            "setBy": "user",
            "date": 1729423115,
            "visitorIp": "77.137.72.126",
            "operatorId": None,
            "personId": "00091551-f021-466e-b75a-765950dcc091"
        },
        "sandbox": False,
        "isDesignMode": False,
        "isProjectOnline": True,
        "cache_hash": "3ad481b29fd8f4ad92577b98f8ba10ce",
        "after_reconnect": False
    }
]

NEW_MESSAGE_FORMAT = [
    "visitorNewMessage",
    {
        "message": None,
        "messageId": "554e01b2-c30b-4308-bbac-bb394b083b46",
        "url": "http://127.0.0.1:8000/tidio.html",
        "visitorId": "457378265e7b4df9a572626386b7a2cd",
        "projectPublicKey": "hdikhrhpbm1frocyeuro1aplei6xxdvz",
        "device": "desktop"
    }
]

import websocket


def on_message(ws, message):
    print(f"Received message: {message}")


def on_error(ws, error):
    print(f"Error: {error}")


def on_close(ws, *args):
    print("Connection closed")


def on_open(ws):
    print("Connection open.")


def get_cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Recursively copy files from multiple source dirs to multiple destination dirs'
    )
    parser.add_argument(
        'src_dest_pairs',
        nargs='+',
        help='Pairs of source and destination paths, each separated by colon like so: /src/path:/dest/path'
    )
    parser.add_argument(
        '-l', '--limit',
        required=False,
        help='Transfer bandwidth limit'
    )
    return parser.parse_args()


def send_msg(ws: websocket.WebSocketApp, msg: list):
    ws.send(json.dumps(msg))


if __name__ == '__main__':
    ws = websocket.WebSocketApp(
        TIDIO_API_URL,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    ws.run_forever()

    # this is what the server does, Not sure if it works.
    ws.send(json.dumps("40"))  # I assume this is some sort of ack.

    # register visitor
    send_msg(ws, VISITOR_REGISTER_FORMAT)
    while True:
        msg_to_send = input("Enter message: ")
        message = NEW_MESSAGE_FORMAT.copy()
        message[1]["message"] = msg_to_send
        send_msg(ws, message)
        print("Message sent")
