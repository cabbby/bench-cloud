#! /usr/bin/python3
import sys, subprocess, time, json, os
from cloudhelper_tencent import *
from tencentcloud.cvm.v20170312 import models

def ssh_try(cmd, name=""):
    while True:
        outp = subprocess.getoutput(cmd)
        if not ("refused" in outp or "closed" in outp or "unavailable" in outp or "denied" in outp):
            break
        print("--- err")
        print(outp)
        print("--- Retry", name)

def run(region, zoneId, confs):
    setRegion(region)

    placement = models.Placement()
    placement.Zone = zoneId

    internetAccessible = models.InternetAccessible()
    internetAccessible.InternetChargeType = "TRAFFIC_POSTPAID_BY_HOUR"
    internetAccessible.PublicIpAssigned = True
    internetAccessible.InternetMaxBandwidthOut = 1

    loginSettings = models.LoginSettings()
    loginSettings.Password = "Wk1Pa0tm"

    params = {
        "InstanceType": "S4.MEDIUM4",
        "InstanceName": "bench-launcher",
        "InstanceChargeType": "POSTPAID_BY_HOUR",
        "Placement": placement,
        "ImageId": getImageId("Ubuntu Server 16.04.1 LTS 64位"),
        "InternetAccessible": internetAccessible,
        "LoginSettings": loginSettings
    }

    print("Creating launcher instance")
    InstanceId = createInstance(params).InstanceIdSet[0]
    waitInstanceStatus(InstanceId, targetStatus="RUNNING", interval=0.1)

    ip = getInstanceAttribute(InstanceId).PublicIpAddresses[0]
    
    print("Setting up")
    ssh_try("sshpass -p 'Wk1Pa0tm' scp -o stricthostkeychecking=no ./files_launcher.tar.gz ubuntu@%s:~/" % ip, "1")
    ssh_try("sshpass -p 'Wk1Pa0tm' ssh -o stricthostkeychecking=no ubuntu@%s 'tar xzvf ~/files_launcher.tar.gz'" % ip, "2")
    ssh_try("sshpass -p 'Wk1Pa0tm' ssh -o stricthostkeychecking=no ubuntu@%s 'cd ~/files_launcher && echo 'Wk1Pa0tm' | sudo -S bash ./prepare_tencent.sh'" % ip, "3")

    if not os.path.exists("./bench_result"):
        os.mkdir("./bench_result")

    for instanceType in confs:
        p = subprocess.Popen("sshpass -p 'Wk1Pa0tm' ssh -o stricthostkeychecking=no ubuntu@%s 'cd ~/files_launcher && python3 -u bench_launcher_tencent.py %s %s'" % (ip, region, instanceType), shell=True, stdout=subprocess.PIPE)
        for line in iter(p.stdout.readline, b''):
            sys.stdout.write(line.decode(sys.stdout.encoding))

        timeStr = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        fn = "bench_result_tencent_%s_%s_%s.txt" % (region, instanceType, timeStr)
        ssh_try("sshpass -p 'Wk1Pa0tm' scp -o stricthostkeychecking=no ubuntu@%s:~/files_launcher/bench_result.txt ./bench_result/%s"  % (ip, fn), "fetch")

    print("Stopping launcher")
    stopInstance(InstanceId)
    waitInstanceStatus(InstanceId, targetStatus="STOPPED", interval=0.1)
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