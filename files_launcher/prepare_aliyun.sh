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

pip3 install aliyun-python-sdk-core-v3 aliyun-python-sdk-ecs

cd netperf-2.7.0
./configure > /dev/null && make > /dev/null && make install > /dev/null