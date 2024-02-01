#!/home/gj/proj/Digital-Transformation-stack-for-evidence-generation/venv/bin/python
#you have to change this

import sys
import json
import struct
from client import EvidenceMaker


# Read a message from stdin and decode it.
def getMessage():
    rawLength = sys.stdin.buffer.read(4)
    if len(rawLength) == 0:
        sys.exit(0)
    messageLength = struct.unpack("@I", rawLength)[0]
    message = sys.stdin.buffer.read(messageLength).decode("utf-8")
    return json.loads(message)


# Encode a message for transmission,
# given its content.
def encodeMessage(messageContent):
    # https://docs.python.org/3/library/json.html#basic-usage
    # To get the most compact JSON representation, you should specify
    # (',', ':') to eliminate whitespace.
    # We want the most compact representation because the browser rejects # messages that exceed 1 MB.
    encodedContent = json.dumps(messageContent, separators=(",", ":")).encode("utf-8")
    encodedLength = struct.pack("@I", len(encodedContent))
    return {"length": encodedLength, "content": encodedContent}


# Send an encoded message to stdout
def sendMessage(encodedMessage):
    sys.stdout.buffer.write(encodedMessage["length"])
    sys.stdout.buffer.write(encodedMessage["content"])
    sys.stdout.buffer.flush()


def main():
    try:
        receivedMessage = getMessage()
        msg = json.loads(receivedMessage)
        url = msg["url"]
        filename = msg["filepath"] + "/evidence"
        evidence_maker = EvidenceMaker(base_path=filename)
        evidence_maker.make(url)
        status = "success"
    except Exception as e:
        status = str(e)
    finally:
        sendMessage(encodeMessage(status))


if __name__ == "__main__":
    main()