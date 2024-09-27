#! /usr/bin/python3
import os
import argparse

parser = argparse.ArgumentParser(
    prog='rf',
    description='read and display the contents of the named fifo',
    epilog="Thanks for using %(prog)s! :)",
)
general = parser.add_argument_group("general output")
general.add_argument("fifotoread", nargs="?", default='./mefifo')

args = parser.parse_args()
pipe_path = args.fifotoread

print(f"Reading the contents of the named pipe: {pipe_path}:")
while True:
    with open(pipe_path) as fifo:
        for line in fifo:
            print(line)
