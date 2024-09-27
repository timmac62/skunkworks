#! /usr/bin/python3
# sender.py
# the sender
import os
import time
import argparse

# Define the path for the named pipe (FIFO)
fifo_path = "/tmp/my_fifo"

parser = argparse.ArgumentParser(
    prog='sender',
    description='send message to the receiver named pipe',
    epilog="Thanks for using %(prog)s! :)",
)
general = parser.add_argument_group("general output")
general.add_argument("message", nargs="?", default='Namaste from sender')
detailed = parser.add_argument_group("detailed output")
detailed.add_argument("-r", "--response", action="store_true")

args = parser.parse_args()
print(args)
message = args.message

if args.response == True:
    print('receive response')

# Ensure the named pipe exists before communicating with it
if not os.path.exists(fifo_path):
    print(f"Named pipe at {fifo_path} does not exist. Please run my_server.py first.")
    exit(1)

# Function to send messages to the server and receive echoes
def sender():
    # Send messages to the server
    with open(fifo_path, 'w') as fifo_write:
        print(f"sender: Sending '{message}'")
        fifo_write.write(message + "\n")
        fifo_write.flush()  # Ensure the message is sent immediately
        time.sleep(1)  # Simulate some delay between messages

if __name__ == "__main__":
    sender()
