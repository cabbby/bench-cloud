#! /usr/bin/python3
import sys, subprocess, time, os
from cloudhelper_aliyun import *

def ssh_try(cmd, name=""):
    while True:
        outp = subprocess.getoutput(cmd)
        if not ("refused" in outp or "closed" in outp or "unavailable" in outp or "denied" in outp):
            break
        print("--- err")
        print(outp)
        print("--- Retry", name)

def run(region, zoneId, confs):
    params = {
        "InstanceType": "ecs.g6.large",
        "ImageId": "ubuntu_16_04_64_20G_alibase_20191112.vhd",
        "InstanceName": "bench-launcher",
        "InternetChargeType": "PayByTraffic",
        "AutoRenew": False,
        "InternetMaxBandwidthOut": 1,
        "Password": "Wk1Pa0tm",
        "SystemDiskSize": 20,
        "SystemDiskCategory": "cloud_efficiency",
        "IoOptimized": "optimized",
        "InstanceChargeType": "PostPaid",
        "ZoneId": zoneId
    }

    setRegion(region)

    print("Creating launcher instance")
    InstanceId = createInstance(params)
    waitInstanceStatus(InstanceId, targetStatus="Stopped", interval=0.1)
    print("Starting launcher")
    startInstance(InstanceId)
    waitInstanceStatus(InstanceId, targetStatus="Running", interval=0.1)
    ip = allocatePublicIpAddress(InstanceId)["IpAddress"]

    print("Setting up")
    ssh_try("sshpass -p 'Wk1Pa0tm' scp -o stricthostkeychecking=no ./files_launcher.tar.gz  root@%s:/root/" % ip, "1")
    ssh_try("sshpass -p 'Wk1Pa0tm' ssh -o stricthostkeychecking=no root@%s 'tar xzvf /root/files_launcher.tar.gz'" % ip, "2")
    ssh_try("sshpass -p 'Wk1Pa0tm' ssh -o stricthostkeychecking=no root@%s 'cd /root/files_launcher && bash ./prepare_aliyun.sh'" % ip, "3")

    if not os.path.exists("./bench_result"):
        os.mkdir("./bench_result")

    for instanceType in confs:
        p = subprocess.Popen("sshpass -p 'Wk1Pa0tm' ssh -o stricthostkeychecking=no root@%s 'cd /root/files_launcher && python3 -u bench_launcher_aliyun.py %s %s'" % (ip, region, instanceType), shell=True, stdout=subprocess.PIPE)
        for line in iter(p.stdout.readline, b''):
            sys.stdout.write(line.decode(sys.stdout.encoding))

        timeStr = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        fn = "bench_result_aliyun_%s_%s_%s.txt" % (region, instanceType, timeStr)
        ssh_try("sshpass -p 'Wk1Pa0tm' scp -o stricthostkeychecking=no root@%s:/root/files_launcher/bench_result.txt ./bench_result/%s"  % (ip, fn), "fetch")

    print("Stopping launcher")
    stopInstance(InstanceId)
    waitInstanceStatus(InstanceId, targetStatus="Stopped", interval=0.1)
    print("Deleting launcher")
    deleteInstance(InstanceId)
    waitInstanceStatus(InstanceId, targetStatus=None, interval=0.1)

if __name__ == "__main__":
    if len(sys.argv) > 3:
        lst = json.loads(sys.argv[3])
        if isinstance(lst, list):
            run(region=sys.argv[1], zoneId=sys.argv[2], confs=lst)
        else:
            print("Invalid arguments")
    else:
        print("Invalid arguments")