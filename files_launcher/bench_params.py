import copy

def getParamSets(info):
    cpu_params = [
        {
            "num_threads": 1,
            "max_requests": 20000,
            "percentile": 98,
            "cpu_max_prime": 10000
        }
    ]

    io_params = [
        {
            "num_threads": 1,
            "max_requests": 20000,
            "percentile": 98,
            "file_test_mode": "seqrd",
            "file_total_size": "2G",
            "file_block_size": "16384",
            "file_num": 128
        },

        {
            "num_threads": 1,
            "max_requests": 20000,
            "percentile": 98,
            "file_test_mode": "seqwr",
            "file_total_size": "2G",
            "file_block_size": "16384",
            "file_num": 128
        },

        {
            "num_threads": 1,
            "max_requests": 20000,
            "percentile": 98,
            "file_test_mode": "rndrd",
            "file_total_size": "2G",
            "file_block_size": "16384",
            "file_num": 128
        },

        {
            "num_threads": 1,
            "max_requests": 20000,
            "percentile": 98,
            "file_test_mode": "rndwr",
            "file_total_size": "2G",
            "file_block_size": "16384",
            "file_num": 128
        },

        {
            "num_threads": 1,
            "max_requests": 20000,
            "percentile": 98,
            "file_test_mode": "rndrw",
            "file_total_size": "2G",
            "file_block_size": "16384",
            "file_num": 128
        }
    ]

    mem_params = [
        {
            "num_threads": 1,
            "percentile": 98,
            "memory_total_size": "100G",
            "memory_block_size": "1K",
            "memory_oper": "read"
        },

        {
            "num_threads": 1,
            "percentile": 98,
            "memory_total_size": "100G",
            "memory_block_size": "1K",
            "memory_oper": "write"
        }
    ]

    param_sets = {
        "cpu": [],
        "io": [],
        "mem": []
    }

    for num_threads in [1, info["cpu_count"]]: 
        for arr in [cpu_params, io_params, mem_params]:
            for p in arr:
                p["num_threads"] = num_threads

        for p in cpu_params:
            param_sets["cpu"].append(copy.deepcopy(p))
        for p in io_params:
            param_sets["io"].append(copy.deepcopy(p))
        for p in mem_params:
            param_sets["mem"].append(copy.deepcopy(p))
        
    return param_sets