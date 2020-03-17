from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.cvm.v20170312 import cvm_client, models
import time

param1, param2 = "", ""

cred = credential.Credential(param1, param2)
client = cvm_client.CvmClient(cred, "ap-beijing")

def setRegion(region):
    global client
    client = cvm_client.CvmClient(cred, region)

def describeImages():
    req = models.DescribeImagesRequest()
    req.Limit = 100
    resp = client.DescribeImages(req)
    return resp

def getImageId(ImageName):
    for img in describeImages().ImageSet:
        if img.ImageName == ImageName:
            return img.ImageId
    return None

def getZones(instanceTypes):
    req = models.DescribeZoneInstanceConfigInfosRequest()
    resp = client.DescribeZoneInstanceConfigInfos(req) 

    zones = {}
    for conf in resp.InstanceTypeQuotaSet:
        if conf.InstanceType in instanceTypes and conf.InstanceChargeType == "POSTPAID_BY_HOUR" and conf.Status == "SELL":
            if not conf.Zone in zones:
                zones[conf.Zone] = []
            zones[conf.Zone].append(conf.InstanceType)

    return zones

def createInstance(params):
    req = models.RunInstancesRequest()
    req.InstanceType = params["InstanceType"]
    req.InstanceName = params["InstanceName"]
    req.Placement = params["Placement"]
    req.ImageId = params["ImageId"]
    req.InstanceChargeType = params["InstanceChargeType"]

    if "VirtualPrivateCloud" in params:
        req.VirtualPrivateCloud = params["VirtualPrivateCloud"]
    if "SecurityGroupIds" in params:
        req.SecurityGroupIds = params["SecurityGroupIds"]
    if "InternetAccessible" in params:
        req.InternetAccessible = params["InternetAccessible"]
    if "LoginSettings" in params:
        req.LoginSettings = params["LoginSettings"]

    resp = client.RunInstances(req)
    return resp

def startInstance(InstanceId):
    req = models.StartInstancesRequest()
    req.InstanceIds = [InstanceId]
    resp = client.StartInstances(req)
    return resp

def stopInstance(InstanceId):
    req = models.StopInstancesRequest()
    req.InstanceIds = [InstanceId]
    resp = client.StopInstances(req)
    return resp

def rebootInstance(InstanceId):
    req = models.RebootInstancesRequest()
    req.InstanceIds = [InstanceId]
    resp = client.RebootInstances(req)
    return resp

def deleteInstance(InstanceId):
    req = models.TerminateInstancesRequest()
    req.InstanceIds = [InstanceId]
    resp = client.TerminateInstances(req)
    return resp

def getInstanceAttribute(InstanceId):
    req = models.DescribeInstancesRequest()
    respFilter = models.Filter()
    respFilter.Name = "instance-id"
    respFilter.Values = [InstanceId]
    req.Filters = [respFilter]
    resp = client.DescribeInstances(req)
    return resp.InstanceSet[0] if resp.TotalCount > 0 else None

def getInstanceStatus(InstanceId):
    attr = getInstanceAttribute(InstanceId)
    return attr.InstanceState if attr != None else None

def getInstancePrivateIp(InstanceId):
    attr = getInstanceAttribute(InstanceId)
    return attr.PrivateIpAddresses[0] if attr != None else None

def getInstanceIdByPrivateIpAddress(PrivateIpAddress):
    req = models.DescribeInstancesRequest()
    respFilter = models.Filter()
    respFilter.Name = "private-ip-address"
    respFilter.Values = [PrivateIpAddress]
    req.Filters = [respFilter]
    resp = client.DescribeInstances(req)
    return resp.InstanceSet[0].InstanceId

def waitInstanceStatus(InstanceId, targetStatus, interval):
    while True:
        cur = getInstanceStatus(InstanceId)
        if cur == targetStatus:
            return
        time.sleep(interval)