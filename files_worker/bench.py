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

def benchmark_cpu(params):
    cmdTemplate = "sysbench --test=cpu run \
                        --num-threads=%(num_threads)s \
                        --max-requests=%(max_requests)s \
                        --percentile=%(percentile)s \
                        --cpu-max-prime=%(cpu_max_prime)s \
                        "
    outp = subprocess.getoutput(cmdTemplate % params)
    return outp

def benchmark_io(params):
    cmdTemplate = "sysbench --test=fileio \
                        --num-threads=%(num_threads)s \
                        --max-requests=%(max_requests)s \
                        --percentile=%(percentile)s \
                        --file-test-mode=%(file_test_mode)s \
                        --file-total-size=%(file_total_size)s \
                        --file-block-size=%(file_block_size)s \
                        --file-num=%(file_num)s \
                        "
    subprocess.getoutput(cmdTemplate % params + " prepare")
    outp = subprocess.getoutput(cmdTemplate % params + " run")
    subprocess.getoutput(cmdTemplate % params + " cleanup")
    return outp

def benchmark_mem(params):
    cmdTemplate = "sysbench --test=memory run \
                        --num-threads=%(num_threads)s \
                        --percentile=%(percentile)s \
                        --memory-total-size=%(memory_total_size)s \
                        --memory-block-size=%(memory_block_size)s \
                        --memory-oper=%(memory_oper)s \
                        "
    outp = subprocess.getoutput(cmdTemplate % params)
    return outp

