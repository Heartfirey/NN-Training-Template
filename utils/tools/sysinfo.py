from pynvml import *


def nvidia_info():
    nvidia_dict = {
        "state": True,
        "nvidia_version": "",
        "nvidia_count": 0,
        "gpus": []
    }
    try:
        nvmlInit()
        nvidia_dict["nvidia_version"] = nvmlSystemGetDriverVersion()
        nvidia_dict["nvidia_count"] = nvmlDeviceGetCount()
        for i in range(nvidia_dict["nvidia_count"]):
            handle = nvmlDeviceGetHandleByIndex(i)
            memory_info = nvmlDeviceGetMemoryInfo(handle)
            gpu = {
                "gpu_name": nvmlDeviceGetName(handle),
                "total": memory_info.total,
                "free": memory_info.free,
                "used": memory_info.used,
                "temperature": f"{nvmlDeviceGetTemperature(handle, 0)}℃",
                "powerStatus": nvmlDeviceGetPowerState(handle)
            }
            nvidia_dict['gpus'].append(gpu)
    except NVMLError as _:
        nvidia_dict["state"] = False
    except Exception as _:
        nvidia_dict["state"] = False
    finally:
        try:
            nvmlShutdown()
        except:
            pass
    return nvidia_dict


def check_gpu_mem_usedRate():
    '''
    Get the gpu_mem_use_rate
    :return:
    '''
    max_rate = 0.0
    while True:
        info = nvidia_info()
        # print(info)
        used = info['gpus'][0]['used']
        tot = info['gpus'][0]['total']
        print(f"GPU0 used: {used}, tot: {tot}, 使用率：{used / tot}")
        if used / tot > max_rate:
            max_rate = used / tot
        print("GPU0 最大使用率：", max_rate)
