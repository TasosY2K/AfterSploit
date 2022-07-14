
try:
    import GPUtil
    from pyadl import *
except:
    pass
from psutil import cpu_count, net_if_addrs, process_iter, virtual_memory, disk_partitions, disk_usage, sensors_battery, win_service_iter, win_service_get, Process, users
from platform import processor, uname
from locale import windows_locale
from datetime import datetime
from requests import get
from ctypes import cast,byref,POINTER,Structure,create_string_buffer,windll,WinDLL
from ctypes import wintypes as w
from struct import pack

def cpu_info() -> list:
    '''
    GET CPU INFORMATION WITH CORES

    cpu = cpu_info()[0] # <class 'str'>
    cpu = cpu_info()[1] # <class 'int'>

    '''
    return [processor(),cpu_count()]

def os_info() -> str:
    '''
    PRINT OPERATING SYSTEM TYPE AND VERSION
    '''
    return uname()._asdict()['system'] + " " + \
    uname()._asdict()['release']  + " " + "v" + \
    uname()._asdict()['version']

def hostname_info() -> str:
    '''
    PRINT HOSTNAME ON TARGET
    '''
    return uname()._asdict()['node']

def users_info() -> list:
    '''
    GET USERS ON SYSTEM AND RETURN AS LIST
    system_users = users_info()
    print(system_users[0]) # SHOULD PRINT THE PRIMARY SYSTEM USER
    '''
    user_array = []
    for user in users():
        user_array.append(user.name)
    return user_array

def ram_in_gb_info() -> dict:
    '''
    GET THE RAM IN GIGABYTES

    ram_total = ram_in_gb_info()['total']
    ram_available = ram_in_gb_info()['available']

    RETURNS:
    <class 'int'>
    '''
    memory = virtual_memory()._asdict()
    for items in memory.items():
        memory.update({items[0]: round(items[1]/1073741824)})
    return memory

def screen_resolution() -> list:
    '''
    GET SCREEN RESOLUTION WITH DPI AWARENESS

    screen_x = screen_resolution()[1]
    screen_y = screen_resolution()[0]
    if screen_x == 1080 and screen_y == 1920:
        print('target is using FULLHD display')
    '''
    user32 = windll.user32
    user32.SetProcessDPIAware()
    [w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
    return [w,h]

def gpu_info() -> list:
    '''
    TRY TO GET GPU INFO AND RETURN AS LIST
    #TODO:
    I DIDN'T DEBUG THE AMD CODE SINCE I USE AN NVIDIA GRAPHICS CARD, COULD BE BUGGY PLEASE CREATE ISSUE IF BUGS FOUND

    gpus = gpu_info()
    if(gpus):
        for gpu in gpus:
            print('GPU: ' + gpu)
    '''
    try:
        nvidia = []
        amd = []
        GPUs = GPUtil.getGPUs()
        if GPUs:
            for gpu in GPUs:
                nvidia.append(gpu.name)
        else:
            amd_gpus = ADLManager.getInstance().getDevices()
            for amd_gpu in amd_gpus:
                amd.append(amd_gpu.adapterName)
    except:
        return False
    if amd:
        return amd
    elif nvidia:
        return nvidia
    else:
        return False

class disks:
    '''
    GET DRIVE LETTERS AND STORAGE CAPACITY KEYS: percentage_used, free_space and total_space
    CORRECT ME IF I AM WRONG: IF ONE DISK HAS THE SAME STORAGE CAPACITY AS ANOTHER BUT ONE SHOWS LESS TOTAL CAPACITY THAT MEANS IT IS MORE WORN OUT

    for index in range(len(disks.drives())):
        print(disks.drives()[index],str(disks.space()[index]['free_space']) + " GB FREE SPACE")
    
    EXAMPLE OUTPUT:

    C:\ 99 GB FREE SPACE
    D:\ 100 GB FREE SPACE
    E:\ 900 GB FREE SPACE

    '''
    def drives() -> list:
        '''
        GET DRIVE LETTERS 
        '''
        disks = []
        for disk in disk_partitions():
            disks.append(disk.device)
        return disks
    def space() -> list:
        '''
        GET STORAGE CAPABILITIES: percentage_used, free_space and total_space
        '''
        disks_info = []
        for disk in disk_partitions():
            disks_info.append(disk_usage(disk.device)._asdict())
        for info in disks_info:
            for item in info.items():
                if item[0] == 'percent':
                    info.update({item[0]: round(item[1])})
                else:
                    info.update({item[0]: round(item[1]/1073741824)})
        for item in disks_info:
            for key in list(item.keys()):
                if key == 'percent':
                    item.update({'percentage_used':item[key]})
                    del item[key]
                elif key == 'free':
                    item.update({'free_space':item[key]})
                    del item[key]
                elif key == 'used':
                    item.update({'used_space':item[key]})
                    del item[key]
                elif key == 'total':
                    item.update({'total_space':item[key]})
                    del item[key]
        return disks_info

def battery_info() -> list:
    '''
    GETS THE BATTERY INFORMATION IF TARGET IS A LAPTOP
    battery = battery_info()
    if(battery_info != False):
        battery_percentage = battery_info()[0] # <class 'int'>
        laptop_charging = battery_info()[1] # True or False
    '''
    battery = sensors_battery()
    if not (battery):
        return False
    else:
        return battery.percentage,battery.power_plugged

def services_info():
    '''
    GET LIST OF ALL WINDOWS SERVICES INSTALLED AS JSON FORMAT

    for service in services_info():
        print(service['display_name']) # returns 'str' when looping
    '''
    for service in win_service_iter():
        info = win_service_get(service.name())
        yield info.as_dict()

class task:
    def list():
        '''
        GET LIST OF ALL WINDOWS PROCESSES INSTALLED AND RETURN GENERATOR OBJECT

        for service in processes_info():
            print(service)
        '''
        try:
            for proc in process_iter():
                processName = proc.name()
                yield processName
        except:
            pass
    def kill(PROCNAME: str)-> int:
        '''
        KILL PROCESS VIA NAME return 0 if succcess if fail return -1
        killer = kill('chome.exe')
        print(kill)

        0
        '''
        try:
            for proc in process_iter():
                # check whether the process name matches
                if proc.name() == PROCNAME:
                    proc.kill()
                    return 0
                else:
                    return -1
        except:
            pass
    def kill_all():
        '''
        TERMINATE EVERYTHING ON THE SYSTEM
        '''
        try:
            for proc in process_iter():
                proc.kill()
        except:
            pass

def environment_info() -> str:
    '''
    GET ENVIRONMENT VARIABLES ON WINDOWS

    print(environment_info()['NUMBER_OF_PROCESSORS'])
    print(type(environment_info()['NUMBER_OF_PROCESSORS']))
    
    8
    <class 'str'>

    '''
    return Process().environ()

def languages_info() -> str:
    '''
    GETS LANGUAGES OF THE COMPUTER
    code = languages_info()
    print(code)
    
    en_US
    '''
    wind = windll.kernel32
    lang = wind.GetUserDefaultUILanguage()
    return windows_locale[lang]

def time_info() -> str:
    '''
    GETS SYSTEM TIME INFORMATION
    time = time_info().split(' ')
    print(time[0])

    00:00:00

    print(time[1])

    AM

    '''
    now = datetime.now()
    current_time = now.strftime("%I:%M:%S %p")
    return current_time

class net:
    def query(Value, Ip=''):
        '''
        EXAMPLES:

        city = net.query('city')
        country = net.query('country')
        ip_address = net.query('ip')
        isp = net.query('isp')
        asn = net.query('as')
        '''
        try:
            r = get(f'http://ip-api.com/json/{Ip}').json()
        except:
            return None
        if(Value == 'ip'):
            return r['query']
        else:
            return r[Value]
    def arp_table()-> zip:
        '''
        GET SYSTEM ARP TABLE AND RETURN AS ZIP GENERATOR OBJECT
        for mac,ip in arp_table():
            print(ip)
        for mac,ip in arp_table():
            geolocation(mac)
        
        CREDIT:
        https://stackoverflow.com/questions/59857314/how-can-i-get-the-arp-table-from-a-windows-machine-using-python
        '''
        mac_addresses = []
        ip_addresses = []
        MAXLEN_PHYSADDR = 8
        TYPE = {1:'other',2:'invalid',3:'dynamic',4:'static'}
        class MIB_IPNETROW(Structure):
            _fields_ = (('dwIndex',w.DWORD),
                        ('dwPhysAddrLen',w.DWORD),
                        ('bPhysAddr',w.BYTE * MAXLEN_PHYSADDR),
                        ('dwAddr',w.DWORD),
                        ('dwType',w.DWORD))
            def __repr__(self):
                ip = pack('<L',self.dwAddr)
                ip = f'{ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}'
                mac = bytes(self.bPhysAddr)[:self.dwPhysAddrLen]
                mac = ':'.join(f'{b:02x}' for b in mac)
                return f"{mac} {ip}"
        def TABLE(n):
            class _MIB_IPNETTABLE(Structure):
                _fields_ = (('dwNumEntries',w.DWORD),
                            ('table',MIB_IPNETROW * n))
            return _MIB_IPNETTABLE
        MIB_IPNETTABLE = TABLE(0)
        dll = WinDLL('iphlpapi')
        dll.GetIpNetTable.argtypes = POINTER(MIB_IPNETTABLE),w.PULONG,w.BOOL
        dll.GetIpNetTable.restype = w.ULONG
        size = w.DWORD(0)
        dll.GetIpNetTable(None,byref(size),True)
        buf = cast(create_string_buffer(b'',size=size.value),POINTER(MIB_IPNETTABLE))
        dll.GetIpNetTable(buf,byref(size),True)
        buf = cast(buf,POINTER(TABLE(buf.contents.dwNumEntries)))
        for t in buf.contents.table:
            if t.dwType != 2 and t.dwPhysAddrLen:
                mac = str(t).split(' ')[0]
                ip = str(t).split(' ')[1]
                mac_addresses.append(mac)
                ip_addresses.append(ip)
        return zip(mac_addresses,ip_addresses)
    def card_info() -> str:
        '''
        GET INTERFACES AND IPV6, IPV4 AND MAC ADDRESSES OF INTERFACES AND PARSE AS A LIST

        for nic,nic_info in net.card_info():
            print('INTERFACE: ' + nic + " -> " + nic_info)
        '''
        for interface, snics in net_if_addrs().items():
            for snic in snics:
                yield(interface,snic.address.replace("-",":"))
    def geo_location():
        '''
        ATTEMPT TO FIND EXACT LOCATION THROUGH BSSID
        '''
        macs = []
        for mac,ip in net.arp_table():
            macs.append(mac)
        for m in macs:
            res = get(f'http://api.mylnikov.org/geolocation/wifi?bssid={m}').text
            print(res)

net.geo_location()