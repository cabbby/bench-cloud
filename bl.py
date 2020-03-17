#! /usr/bin/python3
import sys, subprocess

if __name__ == "__main__":
    if len(sys.argv) > 1:
        t = sys.argv[1].lower()
        if t in ["aliyun", "ucloud", "tencent"]:
            subprocess.Popen(["./bl_%s.py" % t] + sys.argv[2:]).wait()
        else:
            print("Invalid cloud provider")
    else:
        print("Invalid arguments")