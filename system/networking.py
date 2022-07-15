from ctypes import cast, byref, POINTER, Structure, create_string_buffer, windll, WinDLL
from psutil import cpu_count, net_if_addrs, process_iter, virtual_memory, disk_partitions, disk_usage, sensors_battery, win_service_iter, win_service_get, Process, users
from requests import get

class Net:
    def ip_info(self, Value, Ip=""):
        """IP information

        Args:
            Value (str): Type of info to retrieve
            Ip (str, optional): IP to lookup. Defaults to "".

        Returns:
            str: Field value
        
        Examples:
            city = net.query("city")
            country = net.query("country")
            ip_address = net.query("ip")
            isp = net.query("isp")
            asn = net.query("as")
        """
        try:
            r = get(f"http://ip-api.com/json/{Ip}").json()
        except:
            return None
        if(Value == "ip"):
            return r["query"]
        else:
            return r[Value]
        
        
    def arp_table(self)-> zip:
        """System ARP table

        Returns:
            zip: Zip generator object
            
        Example:
            for mac,ip in arp_table():
                print(ip)
            for mac,ip in arp_table():
                geolocation(mac)
        """
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
    
    
    def card_info(self) -> str:
        """IPV6 and IPV4 interfaces and MAC addresses of interfaces

        Returns:
            str: Interfaces and addresses
            
        Example:
            for nic, nic_info in net.card_info():
                print("INTERFACE: " + nic + " -> " + nic_info)
        """
        for interface, snics in net_if_addrs().items():
            for snic in snics:
                yield(interface,snic.address.replace("-", ":"))
                
                
    def geo_location(self):
        """Location determined from BSSID
        """
        macs = []
        for mac, ip in net.arp_table():
            macs.append(mac)
        for m in macs:
            res = get(f"http://api.mylnikov.org/geolocation/wifi?bssid={m}").text
            print(res)