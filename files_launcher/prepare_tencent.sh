#!/bin/bash
while true
do
    apt-get update
    if [[ $? > 0 ]]
    then
        echo "retry"
    else
        echo "ok"
        break
    fi
done

while true
do
    apt-get install sshpass python3-pip -y
    if [[ $? > 0 ]]
    then
        echo "retry"
    else
        echo "ok"
        break
    fi
done

pip3 install -i https://pypi.doubanio.com/simple/ tencentcloud-sdk-python

cd netperf-2.7.0
./configure > /dev/null && make > /dev/null && make install > /dev/null