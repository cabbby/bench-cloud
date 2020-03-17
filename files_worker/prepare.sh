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
    sleep 1
done

while true
do
    apt-get install gcc make sysbench -y
    if [[ $? > 0 ]]
    then
        echo "retry"
    else
        echo "ok"
        break
    fi
    sleep 1
done

cd netperf-2.7.0
./configure && make && make install

cd ..
python3 bench_worker.py & 

exit 0