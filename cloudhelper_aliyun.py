from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526.DescribeImagesRequest import DescribeImagesRequest
from aliyunsdkecs.request.v20140526.DescribeRegionsRequest import DescribeRegionsRequest
from aliyunsdkecs.request.v20140526.DescribeZonesRequest import DescribeZonesRequest
from aliyunsdkecs.request.v20140526.CreateInstanceRequest import CreateInstanceRequest
from aliyunsdkecs.request.v20140526.StopInstanceRequest import StopInstanceRequest
from aliyunsdkecs.request.v20140526.DeleteInstanceRequest import DeleteInstanceRequest
from aliyunsdkecs.request.v20140526.StartInstanceRequest import StartInstanceRequest
from aliyunsdkecs.request.v20140526.DescribeInstanceStatusRequest import DescribeInstanceStatusRequest
from aliyunsdkecs.request.v20140526.DescribeNetworkInterfacesRequest import DescribeNetworkInterfacesRequest
from aliyunsdkecs.request.v20140526.RebootInstanceRequest import RebootInstanceRequest
from aliyunsdkecs.request.v20140526.DescribeInstanceAttributeRequest import DescribeInstanceAttributeRequest
from aliyunsdkecs.request.v20140526.CreateSecurityGroupRequest import CreateSecurityGroupRequest
from aliyunsdkecs.request.v20140526.AllocatePublicIpAddressRequest import AllocatePublicIpAddressRequest
import json, time, socket

param1, param2 = "", ""

client = AcsClient(param1, param2, 'cn-beijing')

def setRegion(region):
    global client
    client = AcsClient(param1, param2, region)

def getImages():
    request = DescribeImagesRequest()
    request.set_accept_format('json')
    response = client.do_action_with_exception(request)
    response = json.loads(str(response, encoding='utf-8'))

    return response

def allocatePublicIpAddress(InstanceId):
    request = AllocatePublicIpAddressRequest()
    request.set_accept_format('json')
    request.set_InstanceId(InstanceId)
    response = client.do_action_with_exception(request)
    response = json.loads(str(response, encoding='utf-8'))
    return response

# print(json.dumps(getImages()["Images"]["Image"], indent=4))

def createInstance(params):
    request = CreateInstanceRequest()
    request.set_accept_format('json')
    
    if "SecurityGroupId" in params:
        request.set_SecurityGroupId(params["SecurityGroupId"])
    if "ZoneId" in params:
        request.set_ZoneId(params["ZoneId"])
    if "VSwitchId" in params:
        request.set_VSwitchId(params["VSwitchId"])

    request.set_ImageId(params["ImageId"])
    request.set_InstanceType(params["InstanceType"])
    
    request.set_InstanceName(params["InstanceName"])
    request.set_InternetChargeType(params["InternetChargeType"])
    request.set_AutoRenew(params["AutoRenew"])
    request.set_InternetMaxBandwidthOut(params["InternetMaxBandwidthOut"])
    request.set_Password(params["Password"])
    
    request.set_SystemDiskSize(params["SystemDiskSize"])
    request.set_SystemDiskCategory(params["SystemDiskCategory"])
    
    request.set_IoOptimized(params["IoOptimized"])
    request.set_InstanceChargeType(params["InstanceChargeType"])

    response = client.do_action_with_exception(request)
    response = json.loads(str(response, encoding='utf-8'))

    return response["InstanceId"]

def createSecurityGroup():
    request = CreateSecurityGroupRequest()
    request.set_accept_format('json')
    response = client.do_action_with_exception(request)
    response = json.loads(str(response, encoding='utf-8'))
    return response

def startInstance(InstanceId):
    request = StartInstanceRequest()
    request.set_accept_format('json')
    request.set_InstanceId(InstanceId)
    response = client.do_action_with_exception(request)
    response = json.loads(str(response, encoding='utf-8'))
    return response

def stopInstance(InstanceId):
    request = StopInstanceRequest()
    request.set_accept_format('json')
    request.set_InstanceId(InstanceId)
    response = client.do_action_with_exception(request)
    response = json.loads(str(response, encoding='utf-8'))
    return response

def rebootInstance(InstanceId):
    request = RebootInstanceRequest()
    request.set_accept_format('json')
    request.set_InstanceId(InstanceId)
    response = client.do_action_with_exception(request)
    response = json.loads(str(response, encoding='utf-8'))
    return response

def deleteInstance(InstanceId):
    request = DeleteInstanceRequest()
    request.set_accept_format('json')
    request.set_InstanceId(InstanceId)
    response = client.do_action_with_exception(request)
    response = json.loads(str(response, encoding='utf-8'))
    return response

def getInstanceStatus(InstanceId):
    request = DescribeInstanceStatusRequest()
    request.set_accept_format('json')
    response = client.do_action_with_exception(request)
    response = json.loads(str(response, encoding='utf-8'))

    for entry in response["InstanceStatuses"]["InstanceStatus"]:
        if entry["InstanceId"] == InstanceId:
            return entry["Status"]

    return None

def getInstanceAttribute(InstanceId):
    request = DescribeInstanceAttributeRequest()
    request.set_accept_format('json')
    request.set_InstanceId(InstanceId)
    response = client.do_action_with_exception(request)
    response = json.loads(str(response, encoding='utf-8'))
    return response

def getInstancePrivateIp(InstanceId):
    request = DescribeNetworkInterfacesRequest()
    request.set_accept_format('json')
    response = client.do_action_with_exception(request)
    response = json.loads(str(response, encoding='utf-8'))

    for entry in response["NetworkInterfaceSets"]["NetworkInterfaceSet"]:
        if entry["InstanceId"] == InstanceId:
            return entry["PrivateIpSets"]["PrivateIpSet"][0]["PrivateIpAddress"]
    
    return None

def getInstanceIdByPrivateIpAddress(PrivateIpAddress):
    request = DescribeNetworkInterfacesRequest()
    request.set_accept_format('json')
    response = client.do_action_with_exception(request)
    response = json.loads(str(response, encoding='utf-8'))

    for entry in response["NetworkInterfaceSets"]["NetworkInterfaceSet"]:
        if entry["PrivateIpSets"]["PrivateIpSet"][0]["PrivateIpAddress"] == PrivateIpAddress:
            return entry["InstanceId"]
    
    return None

def waitInstanceStatus(InstanceId, targetStatus, interval):
    while True:
        cur = getInstanceStatus(InstanceId)
        # print(cur)
        if cur == targetStatus:
            return
        time.sleep(interval)