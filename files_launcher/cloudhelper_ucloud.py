from ucloud.core import exc
from ucloud.client import Client
import json, time, socket

class Logger:
    def __init__(self):
        pass

    def info(self, *args):
        pass

param1, param2 = "", ""

client = Client({
    "region": "cn-bj2",
    "public_key": param1,
    "private_key": param2,
})

client.logger = Logger()

def setRegion(region):
    global client
    client = Client({
        "region": region,
        "public_key": param1,
        "private_key": param2,
    })
    client.logger = Logger()

def describeImages():
    resp = client.uhost().describe_image({
        "Limit": 200
    })
    return resp

def getImageId(ImageName):
    l = list(filter(lambda x: x["ImageName"] == ImageName, describeImages()["ImageSet"]))
    if len(l) > 0:
        return l[0]["ImageId"]
    else:
        return None

def createFirewall(rules):
    resp = client.unet().create_firewall({
        "Name": "bench",
        "Rule": rules
    })
    return resp

def deleteFirewall(fwId):
    resp = client.unet().delete_firewall({
        "FWId": fwId
    })
    return resp

def createInstance(params):
    resp = client.uhost().create_uhost_instance(params)
    return resp

def createNetworkInterface():
    client.uhost().create

def startInstance(InstanceId):
    resp = client.uhost().start_uhost_instance({
        "UHostId": InstanceId
    })
    return resp

def stopInstance(InstanceId):
    resp = client.uhost().stop_uhost_instance({
        "UHostId": InstanceId
    })
    return resp

def rebootInstance(InstanceId):
    resp = client.uhost().reboot_uhost_instance({
        "UHostId": InstanceId
    })
    return resp

def deleteInstance(InstanceId, ReleaseEIP=True):
    resp = client.uhost().terminate_uhost_instance({
        "UHostId": InstanceId,
        "ReleaseEIP": ReleaseEIP
    })
    return resp

def getInstanceStatus(InstanceId):
    resp = client.uhost().describe_uhost_instance()
    for host in resp["UHostSet"]:
        if host["UHostId"] == InstanceId:
            return host["State"]
    return None

def getInstanceAttribute(InstanceId):
    resp = client.uhost().describe_uhost_instance()
    for host in resp["UHostSet"]:
        if host["UHostId"] == InstanceId:
            return host
    return None

def getInstancePrivateIpSet(InstanceId):
    resp = client.uhost().describe_uhost_instance()
    for host in resp["UHostSet"]:
        if host["UHostId"] == InstanceId:
            for ip in host["IPSet"]:
                if ip["Type"] == "Private":
                    return ip
    return None

def getInstancePublicIpSet(InstanceId):
    resp = client.uhost().describe_uhost_instance()
    for host in resp["UHostSet"]:
        if host["UHostId"] == InstanceId:
            for ip in host["IPSet"]:
                if ip["Type"] != "Private":
                    return ip
    return None

def getInstanceIdByPrivateIpAddress(PrivateIpAddress):
    resp = client.uhost().describe_uhost_instance()
    for host in resp["UHostSet"]:
        for ip in host["IPSet"]:
            if ip["Type"] == "Private" and ip["IP"] == PrivateIpAddress:
                return host["UHostId"]
    return None

def waitInstanceStatus(InstanceId, targetStatus, interval):
    while True:
        cur = getInstanceStatus(InstanceId)
        # print(cur)
        if cur == targetStatus:
            return
        time.sleep(interval)
'''
print(getInstanceIdByPrivateIpAddress("10.9.40.133"))
print(json.dumps(getInstanceAttribute("uhost-5q3rprfr"), indent=4))
local_zone_id = getInstanceAttribute("uhost-5q3rprfr")["Zone"]
local_subnet_id = getInstancePrivateIpSet("uhost-5q3rprfr")["SubnetId"]
print(local_zone_id, local_subnet_id)

r = createInstance({
    "Zone": local_zone_id,
    "MachineType": "N",
    "CPU": 1,
    "Memory": 1024,
    "SubnetId": local_subnet_id,
    "ChargeType": "Postpay",
    "ImageId": "uimage-bjnvt1zx",
    "LoginMode": "Password",
    "Password": "Wk1Pa0tm",
    "Disks": [
        {
            "Size": 20,
            "Type": "LOCAL_NORMAL",
            "IsBoot": "True",
        }
    ],
})
print(r)
InstanceId = r["UHostIds"][0]
PrivateIpAddress = r["IPs"][0]
waitInstanceStatus(InstanceId, targetStatus="Running", interval=1)
print(stopInstance(InstanceId))
waitInstanceStatus(InstanceId, targetStatus="Stopped", interval=1)
print(deleteInstance(InstanceId))
'''