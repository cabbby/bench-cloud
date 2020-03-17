#! /usr/bin/python3
import sys, subprocess, time, os
from cloudhelper_ucloud import *

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

    params = {
        "Zone": zoneId,
        "MachineType": "N",
        "CPU": 2,
        "Memory": 4096,
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
        "NetworkInterface": [
            {
                "EIP": {
                    "Bandwidth": 1,
                    "OperatorName": "Bgp" if "cn" in region else "International"
                }
            }
        ],
        # "SecurityGroupId": fwId
    }

    print("Creating launcher instance")
    InstanceId = createInstance(params)["UHostIds"][0]
    waitInstanceStatus(InstanceId, targetStatus="Running", interval=0.1)

    try:
        ip = getInstancePublicIpSet(InstanceId)["IP"]

        print("Setting up")
        ssh_try("sshpass -p 'Wk1Pa0tm' scp -o stricthostkeychecking=no ./files_launcher.tar.gz ubuntu@%s:~/" % ip, "1")
        ssh_try("sshpass -p 'Wk1Pa0tm' ssh -o stricthostkeychecking=no ubuntu@%s 'tar xzvf ~/files_launcher.tar.gz'" % ip, "2")
        ssh_try("sshpass -p 'Wk1Pa0tm' ssh -o stricthostkeychecking=no ubuntu@%s 'cd ~/files_launcher && echo 'Wk1Pa0tm' | sudo -S bash ./prepare_ucloud.sh'" % ip, "3")

        if not os.path.exists("./bench_result"):
            os.mkdir("./bench_result")

        for MachineType, CPU, MEM in confs:
            p = subprocess.Popen("sshpass -p 'Wk1Pa0tm' ssh -o stricthostkeychecking=no ubuntu@%s 'cd ~/files_launcher && python3 -u bench_launcher_ucloud.py %s %s %d %d'" % (ip, region, MachineType, CPU, MEM), shell=True, stdout=subprocess.PIPE)
            for line in iter(p.stdout.readline, b''):
                sys.stdout.write(line.decode(sys.stdout.encoding))

            timeStr = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
            fn = "bench_result_ucloud_%s_%s-%d-%d_%s.txt" % (region, MachineType, CPU, MEM, timeStr)
            ssh_try("sshpass -p 'Wk1Pa0tm' scp -o stricthostkeychecking=no ubuntu@%s:~/files_launcher/bench_result.txt ./bench_result/%s"  % (ip, fn), "fetch")
    finally:
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

