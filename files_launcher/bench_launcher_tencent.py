#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import time, sys, os, socket, json, struct, fcntl, subprocess
import bench_result_parser, bench_remote
from cloudhelper_tencent import *
from tencentcloud.cvm.v20170312 import models

class Logger:
    def __init__(self, filename, rectime=True, stdout=True):
        self.filename = filename
        self.fout = open(filename, "w")
        self.rectime = rectime
        self.stdout = stdout
    
    def __call__(self, *args):
        outpStr = " ".join(list(args))
        if self.rectime:
            timeStr = "[%s]" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            if self.stdout:
                print(timeStr, outpStr)
            self.fout.write(timeStr + " " + outpStr + "\n")
        else:
            if self.stdout:
                print(outpStr)
            self.fout.write(outpStr + "\n")

    def close(self):
        self.fout.close()

log = print

def getIpAddress(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', bytes(ifname[:15], "utf-8"))
    )[20:24])

def getLocalIp():
    return getIpAddress("eth0")

def run_bench_tencent(InstanceType):
    local_instance_id = getInstanceIdByPrivateIpAddress(getLocalIp())
    local_attr = getInstanceAttribute(local_instance_id)

    log("====================================================================")
    log("Launching benchmark task with InstanceType=%s" % InstanceType)
    log("Localhost: %s, %s" % (local_instance_id, getLocalIp()))

    loginSettings = models.LoginSettings()
    loginSettings.Password = "Wk1Pa0tm"

    params = {
        "InstanceType": InstanceType,
        "InstanceName": "bench-test",
        "InstanceChargeType": "POSTPAID_BY_HOUR",
        "Placement": local_attr.Placement,
        "ImageId": getImageId("Ubuntu Server 16.04.1 LTS 64位"),
        "VirtualPrivateCloud": local_attr.VirtualPrivateCloud,
        "SecurityGroupIds": local_attr.SecurityGroupIds,
        "LoginSettings": loginSettings
    }
    
    log("Creating instance")
    InstanceId = createInstance(params).InstanceIdSet[0]
    waitInstanceStatus(InstanceId, targetStatus="RUNNING", interval=0.1)

    log("Finished")
    PrivateIpAddress = getInstancePrivateIp(InstanceId)
    log("InstanceId:", InstanceId)
    log("PrivateIpAddress:", PrivateIpAddress)
    '''
    log("Starting instance")
    startInstance(InstanceId)
    waitInstanceStatus(InstanceId, targetStatus="Running", interval=0.1)
    log("Finished")
    '''

    # restart

    log("Stopping instance")
    while getInstanceStatus(InstanceId) != "STOPPING":
        stopInstance(InstanceId)
        time.sleep(3)
    waitInstanceStatus(InstanceId, targetStatus="STOPPED", interval=0.1)
    log("Finished")

    log("Starting instance")
    timeStart = time.time()
    startInstance(InstanceId)
    waitInstanceStatus(InstanceId, targetStatus="RUNNING", interval=0.1)
    timeEnd = time.time()
    log("Finished")

    log("Setting up")
    while True:
        outp = subprocess.getoutput("sshpass -p 'Wk1Pa0tm' scp -o stricthostkeychecking=no ./files_worker.tar.gz ubuntu@%s:~/" % PrivateIpAddress)
        if not ("refused" in outp or "closed" in outp or "unavailable" in outp or "denied" in outp):
            break
    subprocess.getoutput("sshpass -p 'Wk1Pa0tm' ssh -o stricthostkeychecking=no ubuntu@%s 'tar xzvf ~/files_worker.tar.gz'" % PrivateIpAddress)
    subprocess.Popen("sshpass -p 'Wk1Pa0tm' ssh -o stricthostkeychecking=no ubuntu@%s 'cd ~/files_worker && echo 'Wk1Pa0tm' | sudo -S bash ./prepare.sh > /dev/null 2>&1'" % PrivateIpAddress, shell=True)

    log("====================================================================")
    log("Start running benchmark")
    result = bench_remote.run_bench_remote(PrivateIpAddress, portServer=18500)
    log("Finished")
    log("====================================================================")

    log("Stopping instance")
    stopInstance(InstanceId)
    waitInstanceStatus(InstanceId, targetStatus="STOPPED", interval=0.1)
    log("Finished")

    log("Deleting instance")
    deleteInstance(InstanceId)
    waitInstanceStatus(InstanceId, targetStatus=None, interval=0.1)
    log("Finished")

    log("Benchmark task finished")
    log("====================================================================")

    result["startup_time"] = timeEnd - timeStart
    return result
    

def run_bench(Region, InstanceType):
    global log

    setRegion(Region)

    local_instance_id = getInstanceIdByPrivateIpAddress(getLocalIp())
    local_attr = getInstanceAttribute(local_instance_id)
    local_zone_id = local_attr.Placement.Zone

    log = Logger("bench.log", rectime=True, stdout=True)
    bench_remote.log = log
    resLog = Logger("bench_result.txt", rectime=False, stdout=False)

    result = run_bench_tencent(InstanceType)
    resLog(json.dumps(result, indent=4, sort_keys=True))
    log("Results written to %s" % resLog.filename)

    resLog.close()
    log.close()

if __name__ == "__main__":
    if len(sys.argv) > 2:
        run_bench(Region=sys.argv[1], InstanceType=sys.argv[2])
    else:
        print("Illeagl arguments")