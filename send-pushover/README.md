send-pushover
===============

A small Python script for sending Pushover.net messages

The script uses the Python requests module

    sudo apt-get install python3-requests

The script takes three parameters:

| Parameter | Value |
| :-: | - |
| -a | Pushover Application ID |
| -u | The users device ID |
| -m | the message, you can also set the message by piping data to the script |

Example:

    send-pushover.py -a "Application ID" -u "User ID" -m "This is a test message"

or

    echo "Piped message" | send-pushover.py -a "Application ID" -u "User ID"
