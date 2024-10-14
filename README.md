# SW_ObjectTracker
> Skunk Works Object Tracker

[![python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)

This application runs on the NVidia Jetson Orin, utilizing the camera to detect people, assign them a unique ID and sends that ID with X Y coordinates to an AOS app

![](header.png)

## Development setup

The NVidia Jetson Orin development environment is setup to utilize prebuilt docker containers

**NOTE:**  you can alternatively build these projects from source

These containers include l4tpytorch and many other useful libraries and tools

This application takes advantage of these containers as noted below in the Usage example

## File Descriptions

| File | Description |
| ----------- | ----------- |
| rf.py | IPC mkfifo receiver example | 
| sender.py | IPC mkfifo sender implementation | 
| server.py | Socket UDP simple implementation for testing purposes | 
| object_tracking.py | Jetson Inference application - object tracking and sending ID, X, Y coordinates | 



## Usage example

Execute the following commands to get the Object Tracking application running

```sh
cd ~/Documents/jetson-inference
docker/run.sh -v ~/.bash_aliases:/root/.bash_aliases --volume ~/skunkworks/:/my-object-tracking
python3 /my-object-tracking/server.py
python3 /my-object-tracking/object_tracking.py
```


## Release History

* 0.1.1
    * CHANGE: Changed from IPC/mkfifo to a non blocking socket using UDP, 
    * Note that this requires **server.py** to be up and running but this server does not need to be running in container
* 0.1.0
    * CHANGE: Initial implementation
