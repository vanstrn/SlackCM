import psutil
import nvgpu


def QueryResourceUsages(self):
    """Method which returns information on CPU, CPU RAM and GPU RAM.

    Inputs:
    None

    Outputs:
    res (dict) - A dictionary of the following structure:
    {"Item1":XX,...}
    """
    res = {}
    l = []
    for i in range(avgs):
        l.append(psutil.cpu_percent(0.2))
    res['cpu_avg'] = np.mean(l)
    res['cpu_max'] = np.max(l)

    #Getting Memory Usage
    res['ram'] = psutil.virtual_memory()[2]
    res['swp'] = psutil.swap_memory()[3]

    #Getting GPU Usage:
    gpu_stats = nvgpu.gpu_info()
    for i in range(len(gpu_stats)):
        res['gpu_'+str(i)+'_ram'] = gpu_stats[i]['mem_used_percent']

    return res

def QueryUserResourceUsages(self,avgs=5):
    """Method which looks at CPU and RAM usage of each process and
    assigns it to a user.

    Inputs:
    avgs (int) - Number of averages to take the resource usage over.

    Outputs:
    user (dict) - A nested dictionary of the following structure:
    {"Username1":{"Item1":XX,...},...}
    """
    user = {}
    num = psutil.cpu_count()
    for proc in psutil.process_iter():
        pinfo = proc.as_dict(attrs=['pid', 'name', 'username','cpu_percent','memory_percent'])
        if pinfo['username'] in ['root','systemd-resolve','systemd-timesync','avahi','syslog','messagebus','colord','nvidia-persistenced','whoopsie','kernoops','gdm','rtkit','lp']:
            pinfo['username'] = 'background'
        try:
            user[pinfo['username']]['cpu_percent'] += pinfo['cpu_percent']/num
            user[pinfo['username']]['memory_percent'] += pinfo['memory_percent']
        except:
            user[pinfo['username']] = {'cpu_percent': pinfo['cpu_percent']/num,'memory_percent': pinfo['memory_percent']}

    return user
