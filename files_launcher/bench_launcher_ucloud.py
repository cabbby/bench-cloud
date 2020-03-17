#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import socket, time, json, sys, os, fcntl, struct, subprocess
import bench_result_parser, bench_remote
from cloudhelper_ucloud import *

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

def ssh_try(cmd, name=""):
    while True:
        outp = subprocess.getoutput(cmd)
        if not ("refused" in outp or "closed" in outp or "unavailable" in outp or "denied" in outp):
            print("--- ok", name)
            break
        print("--- err")
        print(outp)
        print("--- Retry", name)

def run_bench_ucloud(MachineType, CPU, MEM):
    local_instance_id = getInstanceIdByPrivateIpAddress(getLocalIp())
    local_zone_id = getInstanceAttribute(local_instance_id)["Zone"]
    local_subnet_id = getInstancePrivateIpSet(local_instance_id)["SubnetId"]
    log("====================================================================")
    log("Launching benchmark task with MachineType=%s, CPU=%d MEM=%d" % (MachineType, CPU, MEM))
    log("Localhost: %s, %s" % (local_instance_id, getLocalIp()))
    params = {
        "Zone": local_zone_id,
        "MachineType": MachineType,
        "CPU": CPU,
        "Memory": MEM,
        "SubnetId": local_subnet_id,
        "ChargeType": "Postpay",
        "ImageId": getImageId("Ubuntu 16.04 64位"),
        "LoginMode": "Password",
        "Password": "Wk1Pa0tm",
        "Disks": [
            {
                "Size": 20,
                "Type": "CLOUD_SSD",
                "IsBoot": "True",
            }
        ],
    }

    log("Creating instance")
    resp = createInstance(params)
    InstanceId = resp["UHostIds"][0]
    waitInstanceStatus(InstanceId, targetStatus="Running", interval=0.1)
    log("Finished")
    PrivateIpAddress = resp["IPs"][0]
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
    stopInstance(InstanceId)
    waitInstanceStatus(InstanceId, targetStatus="Stopped", interval=0.1)
    log("Finished")

    log("Starting instance")
    timeStart = time.time()
    startInstance(InstanceId)
    waitInstanceStatus(InstanceId, targetStatus="Running", interval=0.1)
    timeEnd = time.time()
    log("Finished")

    time.sleep(10)

    log("Setting up")
    ssh_try("sshpass -p 'Wk1Pa0tm' scp -o stricthostkeychecking=no ./files_worker.tar.gz  ubuntu@%s:~/" % PrivateIpAddress, "1")
    ssh_try("sshpass -p 'Wk1Pa0tm' ssh -o stricthostkeychecking=no ubuntu@%s 'tar xzvf ~/files_worker.tar.gz'" % PrivateIpAddress, "2")
    subprocess.Popen("sshpass -p 'Wk1Pa0tm' ssh -o stricthostkeychecking=no ubuntu@%s 'cd ~/files_worker && echo 'Wk1Pa0tm' | sudo -S bash ./prepare.sh' > /dev/null 2>&1" % PrivateIpAddress, shell=True)

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


def run_bench(Region, MachineType, CPU, MEM):
    global log

    setRegion(Region)

    local_instance_id = getInstanceIdByPrivateIpAddress(getLocalIp())
    local_zone_id = getInstanceAttribute(local_instance_id)["Zone"]

    log = Logger("bench.log", rectime=True, stdout=True)
    bench_remote.log = log
    resLog = Logger("bench_result.txt", rectime=False, stdout=False)

    result = run_bench_ucloud(MachineType, CPU, MEM)
    resLog(json.dumps(result, indent=4, sort_keys=True))
    log("Results written to %s" % resLog.filename)

    resLog.close()
    log.close()

if __name__ == "__main__":
    if len(sys.argv) > 4:
        run_bench(Region=sys.argv[1], MachineType=sys.argv[2], CPU=int(sys.argv[3]), MEM=int(sys.argv[4]))
    else:
        print("Illeagl arguments")