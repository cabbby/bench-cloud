#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import subprocess, socket, time, bench, json, multiprocessing, fcntl, struct

portServer = 18500

def log(*args):
    print("[%s]" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), *args)

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', bytes(ifname[:15], "utf-8"))
    )[20:24])

def getLocalIp():
    return get_ip_address("eth0")

netserver_daemon = subprocess.Popen(["netserver"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
s = socket.socket()
s.bind((getLocalIp(), portServer))

log("Listening on %s:%d" % s.getsockname())
s.listen(1)
c, addr = s.accept()
log("Connected to %s:%d" % addr)

while True:
    msg = c.recv(2048).decode("utf-8")
    if msg == "GET_INFO":
        log("GET_INFO")
        c.send(json.dumps({
            "cpu_count": multiprocessing.cpu_count()
        }).encode("utf-8"))
    elif msg == "CLOSE":
        log("CLOSE")
        break
    else:
        log("BENCHMARK")
        data = json.loads(msg)
        if data["type"] == "cpu":
            result = bench.benchmark_cpu(data["params"])
        elif data["type"] == "io":
            result = bench.benchmark_io(data["params"])
        elif data["type"] == "mem":
            result = bench.benchmark_mem(data["params"])

        c.send(json.dumps(result).encode(encoding="utf-8"))

subprocess.getoutput("ps -ef | grep netserver | awk '{print $2}' | xargs kill -9")
c.close()