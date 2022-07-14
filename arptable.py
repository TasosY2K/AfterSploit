from ctypes import cast, WinDLL,byref,POINTER,Structure,create_string_buffer,windll
from ctypes import wintypes as w
from struct import pack


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