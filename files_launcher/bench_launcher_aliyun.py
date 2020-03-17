#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import time, sys, os, socket, json, subprocess
import bench_result_parser, bench_remote
from cloudhelper_aliyun import *

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

def getLocalIp():
    return socket.gethostbyname(socket.gethostname())

def run_bench_aliyun(InstanceType):
    local_instance_id = getInstanceIdByPrivateIpAddress(getLocalIp())
    local_attr = getInstanceAttribute(local_instance_id)
    local_sercurity_group_id = local_attr["SecurityGroupIds"]["SecurityGroupId"][0]
    local_zone_id = local_attr["ZoneId"]
    local_vswitch_id = local_attr["VpcAttributes"]["VSwitchId"]

    log("====================================================================")
    log("Launching benchmark task with InstanceType=%s" % InstanceType)
    params = {
        "InstanceType": InstanceType,
        "ImageId": "ubuntu_16_04_64_20G_alibase_20191112.vhd",
        "InstanceName": "bench-test",
        "ZoneId": local_zone_id,
        "SecurityGroupId": local_sercurity_group_id,
        "VSwitchId": local_vswitch_id,
        "InternetChargeType": "PayByTraffic",
        "AutoRenew": False,
        "InternetMaxBandwidthOut": 1,
        "Password": "Wk1Pa0tm",
        "SystemDiskSize": 20,
        "SystemDiskCategory": "cloud_efficiency",
        "IoOptimized": "optimized",
        "InstanceChargeType": "PostPaid"
    }

    log("Creating instance")
    InstanceId = createInstance(params)
    waitInstanceStatus(InstanceId, targetStatus="Stopped", interval=0.1)
    log("Finished")
    PrivateIpAddress = getInstancePrivateIp(InstanceId)
    log("InstanceId:", InstanceId)
    log("PrivateIpAddress:", PrivateIpAddress)

    time.sleep(2)

    log("Starting instance")
    startInstance(InstanceId)
    waitInstanceStatus(InstanceId, targetStatus="Running", interval=0.1)
    log("Finished")

    # restart
    log("Stopping instance")
    stopInstance(InstanceId)
    waitInstanceStatus(InstanceId, targetStatus="Stopped", interval=0.1)
    log("Finished")

    log("Starting instance")
    timeStart = time.time()
    startInstance(InstanceId)
    waitInstanceStatus(InstanceId, targetStatus="Running", interval=0.1)
    timeEnd = time.time()
    log("Finished")

    log("Setting up")
    while True:
        outp = subprocess.getoutput("sshpass -p 'Wk1Pa0tm' scp -o stricthostkeychecking=no ./files_worker.tar.gz  root@%s:/root/" % PrivateIpAddress)
        if not ("refused" in outp or "closed" in outp or "unavailable" in outp or "denied" in outp):
            break
    subprocess.getoutput("sshpass -p 'Wk1Pa0tm' ssh -o stricthostkeychecking=no root@%s 'tar xzvf /root/files_worker.tar.gz'" % PrivateIpAddress)
    subprocess.Popen("sshpass -p 'Wk1Pa0tm' ssh -o stricthostkeychecking=no root@%s 'cd /root/files_worker && bash ./prepare.sh > /dev/null 2>&1'" % PrivateIpAddress, shell=True)

    log("====================================================================")
    log("Start running benchmark")
    result = bench_remote.run_bench_remote(PrivateIpAddress, portServer=18500)
    log("Finished")
    log("====================================================================")

    log("Stopping instance")
    stopInstance(InstanceId)
    waitInstanceStatus(InstanceId, targetStatus="Stopped", interval=0.1)
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
    local_zone_id = local_attr["ZoneId"]

    log = Logger("bench.log", rectime=True, stdout=True)
    bench_remote.log = log
    resLog = Logger("bench_result.txt", rectime=False, stdout=False)

    result = run_bench_aliyun(InstanceType)
    resLog(json.dumps(result, indent=4, sort_keys=True))
    log("Results written to %s" % resLog.filename)

    resLog.close()
    log.close()

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        run_bench(Region=sys.argv[1], InstanceType=sys.argv[2])
    else:
        print("Illeagl arguments")