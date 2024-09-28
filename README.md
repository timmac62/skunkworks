# skunkworks
Jetson Nano Object Tracking


use alias to run the container:
alias ot='ji; docker/run.sh -v ~/.bash_aliases:/root/.bash_aliases --volume ~/skunkworks/:/my-object-tracking'

execute the code:
py /my-object-tracking/object_tracking.py
