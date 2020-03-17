import socket, json, time, subprocess, re, struct, fcntl
import bench_params, bench_result_parser

log = print

def socketReq(s, params):
    s.send(params.encode("utf-8"))
    return json.loads(s.recv(20480).decode("utf-8"))

def getIpAddress(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', bytes(ifname[:15], "utf-8"))
    )[20:24])

def getLocalIp():
    return getIpAddress("eth0")

def run_bench_remote(hostServer, portServer):
    intervalRetry = 0.2
    s = socket.socket()
    s.bind((getLocalIp(), 0))

    log("Opening connection on %s:%d" % s.getsockname())
    try:
        while True:
            try:
                s.connect((hostServer, portServer))
            except Exception as err:
                time.sleep(intervalRetry)
            else:
                break

        log("Connected to %s:%d" % (hostServer, portServer))

        result = {"cpu": [], "io": [], "mem": []}
        paramSets = bench_params.getParamSets(socketReq(s, "GET_INFO"))
        for key in paramSets.keys():
            log("Benchmark-%s : Running" % key.upper())
            for params in paramSets[key]:
                msg = json.dumps({
                    "type": key,
                    "params": params
                })
                result_text = socketReq(s, msg)
                result[key].append(bench_result_parser.parse[key](params, result_text))

        test_time = 10
        log("Benchmark-NET : Running")
        outp1 = subprocess.getoutput("netperf -H %s -l %d -t TCP_STREAM" % (hostServer, test_time))
        outp2 = subprocess.getoutput("netperf -H %s -l %d -t TCP_RR" % (hostServer, test_time))
        outp3 = subprocess.getoutput("netperf -H %s -l %d -t UDP_STREAM" % (hostServer, test_time))
        outp4 = subprocess.getoutput("netperf -H %s -l %d -t UDP_RR" % (hostServer, test_time))
        result["net"] = {
            "TCP_STREAM": float(re.findall("[\d]+[.\d]*", outp1)[-1:][0]),
            "TCP_RR": float(re.findall("[\d]+[.\d]*", outp2)[-3:][0]),
            "UDP_STREAM": float(re.findall("[\d]+[.\d]*", outp3)[-1:][0]),
            "UDP_RR": float(re.findall("[\d]+[.\d]*", outp4)[-3:][0])
        }
    finally:
        s.send("CLOSE".encode("utf-8"))
        s.close()
        log("Connection closed")
    
    return result