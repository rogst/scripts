#!/usr/bin/env python3

import argparse
import requests
import sys

def push_message(message, app, user):
        data = { "token": app, "user": user, "message": message }
        r = requests.post("https://api.pushover.net/1/messages.json", params=data)

def main(argv):
    parser = argparse.ArgumentParser(description="Push message with Pushover.net")
    parser.add_argument('-a', dest='app_id', required=True, help="Application ID")
    parser.add_argument('-u', dest='user_id', required=True, help="User ID")
    parser.add_argument('-m', dest='message', required=False, default='', help="Message to send, can also be read from stdin")
    args = parser.parse_args(argv)

    if (args.message == '') and not sys.stdin.isatty():
        for line in sys.stdin:
            args.message = args.message + line

    push_message(args.message, args.app_id, args.user_id)

if __name__ == "__main__":
    main(sys.argv[1:])