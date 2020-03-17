import subprocess, re, multiprocessing, time, copy

def log(*args):
    print("[%s]" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), *args)

def ps(pattern, string, conv=None):
    res = re.search(pattern, string)
    if res == None:
        return res
    res = res.group()
    if conv != None:
        res = conv(res)
    return res

def parse_cpu(params, outp):
    outp = " ".join(outp.split())
    result = {
        "params": copy.deepcopy(params),
        "total_time": ps("(?<=total time: )[.\d]*[\w]*", outp),
        "per_request": {
            "min": ps("(?<=min: )[.\d]*[\w]*", outp),
            "max": ps("(?<=max: )[.\d]*[\w]*", outp),
            "avg": ps("(?<=avg: )[.\d]*[\w]*", outp),
            "approx_percentile": ps("(?<=percentile: )[.\d]*[\w]*", outp),
        },
        "threads_fairness": {
            "events": {
                "avg": float(ps("(?<=events \(avg/stddev\): )[./\d]*", outp).split("/")[0]),
                "stddev": float(ps("(?<=events \(avg/stddev\): )[./\d]*", outp).split("/")[1])
            },
            "exec_time": {
                "avg": float(ps("(?<=time \(avg/stddev\): )[./\d]*", outp).split("/")[0]),
                "stddev": float(ps("(?<=time \(avg/stddev\): )[./\d]*", outp).split("/")[1])
            }
        }
    }
    return result

def parse_io(params, outp):
    outp = " ".join(outp.split());
    result = {
        "params": copy.deepcopy(params),
        "transfer_rate": ps("[.\d]*[GMK]b/sec", outp),
        "total_time": ps("(?<=total time: )[.\d]*[\w]*", outp),
        "per_request": {
            "min": ps("(?<=min: )[.\d]*[\w]*", outp),
            "max": ps("(?<=max: )[.\d]*[\w]*", outp),
            "avg": ps("(?<=avg: )[.\d]*[\w]*", outp),
            "approx_percentile": ps("(?<=percentile: )[.\d]*[\w]*", outp),
        },
        "threads_fairness": {
            "events": {
                "avg": float(ps("(?<=events \(avg/stddev\): )[./\d]*", outp).split("/")[0]),
                "stddev": float(ps("(?<=events \(avg/stddev\): )[./\d]*", outp).split("/")[1])
            },
            "exec_time": {
                "avg": float(ps("(?<=time \(avg/stddev\): )[./\d]*", outp).split("/")[0]),
                "stddev": float(ps("(?<=time \(avg/stddev\): )[./\d]*", outp).split("/")[1])
            }
        }
    }
    return result

def parse_mem(params, outp):
    outp = " ".join(outp.split());
    result = {
        "params": copy.deepcopy(params),
        "transfer_rate": "".join(ps("[.\d]* [GMK]B/sec", outp).split(" ")),
        "total_time": ps("(?<=total time: )[.\d]*[\w]*", outp),
        "per_request": {
            "min": ps("(?<=min: )[.\d]*[\w]*", outp),
            "max": ps("(?<=max: )[.\d]*[\w]*", outp),
            "avg": ps("(?<=avg: )[.\d]*[\w]*", outp),
            "approx_percentile": ps("(?<=percentile: )[.\d]*[\w]*", outp),
        },
        "threads_fairness": {
            "events": {
                "avg": float(ps("(?<=events \(avg/stddev\): )[./\d]*", outp).split("/")[0]),
                "stddev": float(ps("(?<=events \(avg/stddev\): )[./\d]*", outp).split("/")[1])
            },
            "exec_time": {
                "avg": float(ps("(?<=time \(avg/stddev\): )[./\d]*", outp).split("/")[0]),
                "stddev": float(ps("(?<=time \(avg/stddev\): )[./\d]*", outp).split("/")[1])
            }
        }
    }
    return result

parse = {
    "cpu": parse_cpu,
    "io": parse_io,
    "mem": parse_mem
}