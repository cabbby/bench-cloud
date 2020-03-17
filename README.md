# bench-cloud

### Usage

``` bash
./bl.py aliyun cn-beijing cn-beijing-g '["ecs.g6.large", "ecs.c6.xlarge", "ecs.r6.large"]'

./bl.py tencent ap-beijing ap-beijing-4 '["S4.MEDIUM8","C3.LARGE8","M5.MEDIUM16"]'

./bl.py ucloud cn-bj2 cn-bj2-02 '[["N",2,8192],["N",4,8192],["N",2,16384]]'
```

### Result example

```
{
    "cpu": [
        {
            "params": {
                "cpu_max_prime": 10000,
                "max_requests": 20000,
                "num_threads": 1,
                "percentile": 98
            },
            "per_request": {
                "approx_percentile": "0.91ms",
                "avg": "0.91ms",
                "max": "6.69ms",
                "min": "0.90ms"
            },
            "threads_fairness": {
                "events": {
                    "avg": 20000.0,
                    "stddev": 0.0
                },
                "exec_time": {
                    "avg": 18.1316,
                    "stddev": 0.0
                }
            },
            "total_time": "18.1336s"
        },
        {
            "params": {
                "cpu_max_prime": 10000,
                "max_requests": 20000,
                "num_threads": 4,
                "percentile": 98
            },
            "per_request": {
                "approx_percentile": "1.13ms",
                "avg": "1.09ms",
                "max": "17.04ms",
                "min": "0.90ms"
            },
            "threads_fairness": {
                "events": {
                    "avg": 5000.0,
                    "stddev": 16.99
                },
                "exec_time": {
                    "avg": 5.4714,
                    "stddev": 0.01
                }
            },
            "total_time": "5.4764s"
        }
    ],
    "io": [
        {
            "params": {
                "file_block_size": "16384",
                "file_num": 128,
                "file_test_mode": "seqrd",
                "file_total_size": "2G",
                "max_requests": 20000,
                "num_threads": 1,
                "percentile": 98
            },
            "per_request": {
                "approx_percentile": "0.00ms",
                "avg": "0.00ms",
                "max": "0.03ms",
                "min": "0.00ms"
            },
            "threads_fairness": {
                "events": {
                    "avg": 131072.0,
                    "stddev": 0.0
                },
                "exec_time": {
                    "avg": 0.3753,
                    "stddev": 0.0
                }
            },
            "total_time": "0.3868s",
            "transfer_rate": "5.1711Gb/sec"
        },
        {
            "params": {
                "file_block_size": "16384",
                "file_num": 128,
                "file_test_mode": "seqwr",
                "file_total_size": "2G",
                "max_requests": 20000,
                "num_threads": 1,
                "percentile": 98
            },
            "per_request": {
                "approx_percentile": "0.01ms",
                "avg": "0.06ms",
                "max": "188.21ms",
                "min": "0.01ms"
            },
            "threads_fairness": {
                "events": {
                    "avg": 131072.0,
                    "stddev": 0.0
                },
                "exec_time": {
                    "avg": 7.2116,
                    "stddev": 0.0
                }
            },
            "total_time": "20.2111s",
            "transfer_rate": "101.33Mb/sec"
        },
        {
            "params": {
                "file_block_size": "16384",
                "file_num": 128,
                "file_test_mode": "rndrd",
                "file_total_size": "2G",
                "max_requests": 20000,
                "num_threads": 1,
                "percentile": 98
            },
            "per_request": {
                "approx_percentile": "0.00ms",
                "avg": "0.00ms",
                "max": "0.04ms",
                "min": "0.00ms"
            },
            "threads_fairness": {
                "events": {
                    "avg": 20000.0,
                    "stddev": 0.0
                },
                "exec_time": {
                    "avg": 0.0634,
                    "stddev": 0.0
                }
            },
            "total_time": "0.0657s",
            "transfer_rate": "4.6442Gb/sec"
        },
        {
            "params": {
                "file_block_size": "16384",
                "file_num": 128,
                "file_test_mode": "rndwr",
                "file_total_size": "2G",
                "max_requests": 20000,
                "num_threads": 1,
                "percentile": 98
            },
            "per_request": {
                "approx_percentile": "0.01ms",
                "avg": "0.01ms",
                "max": "0.04ms",
                "min": "0.00ms"
            },
            "threads_fairness": {
                "events": {
                    "avg": 20000.0,
                    "stddev": 0.0
                },
                "exec_time": {
                    "avg": 0.1514,
                    "stddev": 0.0
                }
            },
            "total_time": "10.1158s",
            "transfer_rate": "30.892Mb/sec"
        },
        {
            "params": {
                "file_block_size": "16384",
                "file_num": 128,
                "file_test_mode": "rndrw",
                "file_total_size": "2G",
                "max_requests": 20000,
                "num_threads": 1,
                "percentile": 98
            },
            "per_request": {
                "approx_percentile": "0.01ms",
                "avg": "0.01ms",
                "max": "0.04ms",
                "min": "0.00ms"
            },
            "threads_fairness": {
                "events": {
                    "avg": 20000.0,
                    "stddev": 0.0
                },
                "exec_time": {
                    "avg": 0.1072,
                    "stddev": 0.0
                }
            },
            "total_time": "4.4976s",
            "transfer_rate": "69.481Mb/sec"
        },
        {
            "params": {
                "file_block_size": "16384",
                "file_num": 128,
                "file_test_mode": "seqrd",
                "file_total_size": "2G",
                "max_requests": 20000,
                "num_threads": 4,
                "percentile": 98
            },
            "per_request": {
                "approx_percentile": "0.01ms",
                "avg": "0.01ms",
                "max": "2.57ms",
                "min": "0.00ms"
            },
            "threads_fairness": {
                "events": {
                    "avg": 32767.75,
                    "stddev": 13185.29
                },
                "exec_time": {
                    "avg": 0.1656,
                    "stddev": 0.07
                }
            },
            "total_time": "0.2171s",
            "transfer_rate": "9.2113Gb/sec"
        },
        {
            "params": {
                "file_block_size": "16384",
                "file_num": 128,
                "file_test_mode": "seqwr",
                "file_total_size": "2G",
                "max_requests": 20000,
                "num_threads": 4,
                "percentile": 98
            },
            "per_request": {
                "approx_percentile": "0.04ms",
                "avg": "0.23ms",
                "max": "207.41ms",
                "min": "0.01ms"
            },
            "threads_fairness": {
                "events": {
                    "avg": 32768.0,
                    "stddev": 8732.52
                },
                "exec_time": {
                    "avg": 7.4857,
                    "stddev": 0.0
                }
            },
            "total_time": "21.0399s",
            "transfer_rate": "97.339Mb/sec"
        },
        {
            "params": {
                "file_block_size": "16384",
                "file_num": 128,
                "file_test_mode": "rndrd",
                "file_total_size": "2G",
                "max_requests": 20000,
                "num_threads": 4,
                "percentile": 98
            },
            "per_request": {
                "approx_percentile": "0.01ms",
                "avg": "0.01ms",
                "max": "5.90ms",
                "min": "0.00ms"
            },
            "threads_fairness": {
                "events": {
                    "avg": 5093.0,
                    "stddev": 483.86
                },
                "exec_time": {
                    "avg": 0.0289,
                    "stddev": 0.0
                }
            },
            "total_time": "0.0307s",
            "transfer_rate": "10.115Gb/sec"
        },
        {
            "params": {
                "file_block_size": "16384",
                "file_num": 128,
                "file_test_mode": "rndwr",
                "file_total_size": "2G",
                "max_requests": 20000,
                "num_threads": 4,
                "percentile": 98
            },
            "per_request": {
                "approx_percentile": "0.02ms",
                "avg": "0.02ms",
                "max": "43.49ms",
                "min": "0.00ms"
            },
            "threads_fairness": {
                "events": {
                    "avg": 5035.0,
                    "stddev": 497.5
                },
                "exec_time": {
                    "avg": 0.0758,
                    "stddev": 0.02
                }
            },
            "total_time": "10.2091s",
            "transfer_rate": "30.824Mb/sec"
        },
        {
            "params": {
                "file_block_size": "16384",
                "file_num": 128,
                "file_test_mode": "rndrw",
                "file_total_size": "2G",
                "max_requests": 20000,
                "num_threads": 4,
                "percentile": 98
            },
            "per_request": {
                "approx_percentile": "0.01ms",
                "avg": "0.01ms",
                "max": "0.73ms",
                "min": "0.00ms"
            },
            "threads_fairness": {
                "events": {
                    "avg": 5037.0,
                    "stddev": 240.87
                },
                "exec_time": {
                    "avg": 0.0453,
                    "stddev": 0.0
                }
            },
            "total_time": "4.2151s",
            "transfer_rate": "74.687Mb/sec"
        }
    ],
    "mem": [
        {
            "params": {
                "memory_block_size": "1K",
                "memory_oper": "read",
                "memory_total_size": "100G",
                "num_threads": 1,
                "percentile": 98
            },
            "per_request": {
                "approx_percentile": "0.00ms",
                "avg": "0.00ms",
                "max": "1.04ms",
                "min": "0.00ms"
            },
            "threads_fairness": {
                "events": {
                    "avg": 104857600.0,
                    "stddev": 0.0
                },
                "exec_time": {
                    "avg": 16.2029,
                    "stddev": 0.0
                }
            },
            "total_time": "22.5250s",
            "transfer_rate": "4546.07MB/sec"
        },
        {
            "params": {
                "memory_block_size": "1K",
                "memory_oper": "write",
                "memory_total_size": "100G",
                "num_threads": 1,
                "percentile": 98
            },
            "per_request": {
                "approx_percentile": "0.00ms",
                "avg": "0.00ms",
                "max": "0.02ms",
                "min": "0.00ms"
            },
            "threads_fairness": {
                "events": {
                    "avg": 104857600.0,
                    "stddev": 0.0
                },
                "exec_time": {
                    "avg": 25.0767,
                    "stddev": 0.0
                }
            },
            "total_time": "31.3950s",
            "transfer_rate": "3261.66MB/sec"
        },
        {
            "params": {
                "memory_block_size": "1K",
                "memory_oper": "read",
                "memory_total_size": "100G",
                "num_threads": 4,
                "percentile": 98
            },
            "per_request": {
                "approx_percentile": "0.00ms",
                "avg": "0.00ms",
                "max": "4.93ms",
                "min": "0.00ms"
            },
            "threads_fairness": {
                "events": {
                    "avg": 26214400.0,
                    "stddev": 450159.06
                },
                "exec_time": {
                    "avg": 15.4817,
                    "stddev": 0.08
                }
            },
            "total_time": "30.0597s",
            "transfer_rate": "3406.55MB/sec"
        },
        {
            "params": {
                "memory_block_size": "1K",
                "memory_oper": "write",
                "memory_total_size": "100G",
                "num_threads": 4,
                "percentile": 98
            },
            "per_request": {
                "approx_percentile": "0.00ms",
                "avg": "0.00ms",
                "max": "6.11ms",
                "min": "0.00ms"
            },
            "threads_fairness": {
                "events": {
                    "avg": 26214400.0,
                    "stddev": 500259.52
                },
                "exec_time": {
                    "avg": 21.1774,
                    "stddev": 0.07
                }
            },
            "total_time": "34.3375s",
            "transfer_rate": "2982.16MB/sec"
        }
    ],
    "net": {
        "TCP_RR": 9188.63,
        "TCP_STREAM": 3378.16,
        "UDP_RR": 9465.97,
        "UDP_STREAM": 3013.68
    },
    "startup_time": 12.738173246383667
}

```