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

class SystemInfo:
    def cpu_info(self) -> list:
        """CPU information with cores

        Returns:
            list: CPU information with cores
        
        Examples:
            cpu_info()[0] # <class 'str'>
            cpu_info()[1] # <class 'int'> 
        """
        return [processor(), cpu_count()]


    def os_info(self) -> str:
        """Operating system type and version

        Returns:
            str: Operating system type and version
        """
        return uname()._asdict()["system"] + " " + \
        uname()._asdict()["release"]  + " " + "v" + \
        uname()._asdict()["version"]


    def hostname_info(self) -> str:
        """Hostname of target

        Returns:
            str: Hostname of target
        """
        return uname()._asdict()["node"]


    def users_info(self) -> list:
        """Users on system

        Returns:
            list: Users on system
        """
        user_array = []
        for user in users():
            user_array.append(user.name)
        return user_array
    

    def ram_in_gb_info(self) -> dict:
        """RAM in gigabytes

        Returns:
            dict: RAM in gigabytes
            
        Examples:
            ram_in_gb_info()["total"] # <class 'int'>
            ram_in_gb_info()["available"] # <class 'int'>
        """
        memory = virtual_memory()._asdict()
        for items in memory.items():
            memory.update({items[0]: round(items[1]/1073741824)})
        return memory


    def screen_resolution(self) -> list:
        """Screen resolution with DPI awereness

        Returns:
            list: Screen resolution with DPI awereness
        
        Examples:
            screen_x = screen_resolution()[1]
            screen_y = screen_resolution()[0]
            if screen_x == 1080 and screen_y == 1920:
                print("target is using FULLHD display")
        """
        user32 = windll.user32
        user32.SetProcessDPIAware()
        [w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
        return [w,h]


    def gpu_info(self) -> list:
        """GPU info

        Returns:
            list: GPU info
            
        Examples:
            gpus = gpu_info()
            if(gpus):
                for gpu in gpus:
                    print("GPU: " + gpu)
        """
        #TODO: I DIDN'T DEBUG THE AMD CODE SINCE I USE AN NVIDIA GRAPHICS CARD, COULD BE BUGGY PLEASE CREATE ISSUE IF BUGS FOUND
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


def battery_info(self) -> list:
    """Battery information (only on laptops)

    Returns:
        list: Battery information
    
    Example:
        battery = battery_info()
        if(battery_info != False):
            battery_percentage = battery_info()[0] # <class 'int'>
            laptop_charging = battery_info()[1] # True or False
    """
    battery = sensors_battery()
    if not (battery):
        return False
    else:
        return battery.percentage,battery.power_plugged


def services_info(self):
    """All Windows services installed on target

    Yields:
        dict: All Windows services installed on target
        
    Example:
        for service in services_info():
            print(service['display_name']) # returns 'str' when looping
    """
    for service in win_service_iter():
        info = win_service_get(service.name())
        yield info.as_dict()


def environment_info(self) -> list:
    """Enviroment variables

    Returns:
        list: All Windows enviroment variables
    
    Example:
        print(environment_info()["NUMBER_OF_PROCESSORS"]) # 8 <class 'str'>
    """
    return Process().environ()


def languages_info(self) -> str:
    """Languages installed on target

    Returns:
        str: Languages installed on target
        
    Example:
        code = languages_info()
        print(code) # en_US
    """
    wind = windll.kernel32
    lang = wind.GetUserDefaultUILanguage()
    return windows_locale[lang]


def time_info(self) -> str:
    """System time information

    Returns:
        str: System time information
    
    Example:
        time = time_info().split(" ")
        print(time[0]) # 00:00:00
        print(time[1]) # AM
    """
    now = datetime.now()
    current_time = now.strftime("%I:%M:%S %p")
    return current_time