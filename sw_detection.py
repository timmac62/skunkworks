#!/usr/bin/env python3
from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput
import os
import errno

fifo_path = "/tmp/Jetson_FIFO_AOS"

def init_system():
    # Ensure the named pipe exists before communicating with it
    if not os.path.exists(fifo_path):
        print(f"Named pipe at {fifo_path} does not exist!")
        os.mkfifo(fifo_path)

def sendmessage(message):
    # # Send messages to the server
    # print(f"sender: Sending '{message}'")

    # with open(fifo_path, 'w' | os.O_NONBLOCK | os.O_WRONLY) as fifo_write:
    #     print(f"sender: Sending '{message}'")
    #     fifo_write.write(message + "\n")
    #     fifo_write.flush()  # Ensure the message is sent immediately
    #     time.sleep(1)  # Simulate some delay between messages
    try:
        fifo_fd = os.open(fifo_path, os.O_WRONLY | os.O_NONBLOCK)
        os.write(fifo_fd, message.encode())
        print(f"sendMessage: {message.encode()}")
    except OSError as e:
        if e.errno == errno.ENXIO:
            print("no reader")
        else:
            print(f"Error: {e}")
    finally:
        if 'fifo_fd' in locals():
            os.close(fifo_fd)


def object_detection():
    # open detectNet with specified model and threshold
    net = detectNet("ssd-mobilenet-v2", threshold=0.5)

    # camera = videoSource("csi://0")      # '/dev/video0' for V4L2
    camera = videoSource("/dev/video0")      # '/dev/video0' for V4L2
    display = videoOutput("display://0") # 'my_video.mp4' for file

    # capture image frames
    while display.IsStreaming():
        img = camera.Capture()

        if img is None: # capture timeout
            continue

        detections = net.Detect(img)
        for detection in detections:
            detection_message = f"Detected {net.GetClassDesc(detection.ClassID)} with confidence {detection.Confidence:.2f} at top-left ({detection.Left:.0f}, {detection.Top:.0f})"
            sendmessage(detection_message)
            # print(f"Detected {net.GetClassDesc(detection.ClassID)} with confidence {detection.Confidence:.2f} at top-left ({detection.Left:.0f}, {detection.Top:.0f})")
            print(detection_message)
        
        display.Render(img)
        display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))

if __name__ == "__main__":
    init_system()
    object_detection()