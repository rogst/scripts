send-xmpp
===============

A small Python script for sending XMPP messages

The script uses the Python XMPP module, which I installed from the debian repository

    sudo apt-get install python-xmpp

The script takes four parameters:

| Parameter | Value |
| :---: | --- |
| -c | contact to send the message to |
| -u | the user to send the message from |
| -p | the password for the user |
| -m | the message, you can also set the message by piping data to the script |

Example:

    scriptname.py -c "recipient@example.com" -u "sender@example.com" -p "secret" -m "This is a test message"

or

    echo "Piped message" | scriptname.py -c "recipient@example.com" -u "sender@example.com" -p "secret"
