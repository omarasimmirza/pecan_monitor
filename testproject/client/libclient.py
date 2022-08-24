from pysnmp.entity.rfc3413.oneliner import cmdgen
import time
from cryptography.fernet import Fernet
import socket 

ip = socket.gethostbyname(socket.gethostname())
_oid_hrProcessorLoad_ = '1.3.6.1.2.1.25.3.3.1.2'
_oid_cpuRawIdleTime_ = '1.3.6.1.4.1.2021.11.53'
_oid_memTotalReal_ = '1.3.6.1.4.1.2021.4.5'
_oid_memAvailReal_ = '1.3.6.1.4.1.2021.4.6'
_oid_total_uptime = '1.3.6.1.2.1.1.3'

class Stats:
    def __init__(self, memory_used=None, cpu_used=None, total_uptime=None, encrypted=None, key=None):
        self.memory_used = memory_used
        self.cpu_used = cpu_used
        self.total_uptime = total_uptime
        self.encrypted = encrypted
        self.key = key

    def abs_int(num):
        if num < 0:
            return -1 * num
        return num
    def get_data(slef, oid):
        results = []
        cmdGen = cmdgen.CommandGenerator()
        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.nextCmd(
            cmdgen.CommunityData('public'),
            cmdgen.UdpTransportTarget((ip, 161)),
            oid
        )
        if errorIndication:
            print(errorIndication)
        else:
            if errorStatus:
                print('%s at %s' %(
                    errorStatus.prettyPrint(),
                    errorIndex and varBinds[int(errorIndex)-1] or '?'
                ))
            else:
                for lines in varBinds:
                    for name, val in lines:
                        results.append(val)
            if len(results) == 1:
                return results[0]
            else:
                return results

    def cpu_usage(self):
        try:
            idle_time1 = float(self.get_data(_oid_cpuRawIdleTime_))
            time.sleep(7)
            idle_time2 = float(self.get_data(_oid_cpuRawIdleTime_))
            if isinstance(self.get_data(_oid_hrProcessorLoad_), list):
                core_load = len(self.get_data(_oid_hrProcessorLoad_))
            else:
                core_load = 1
            self.cpu_used = 100.0 - ((idle_time2 - idle_time1) / core_load / 5.0)
            self.cpu_used = 0.0 if self.cpu_used < 0.0 else self.cpu_used
        except Exception as e:
            print(e)

    def ram_usage(self):
        try:
            total_ram = float(self.get_data(_oid_memTotalReal_))
            avail_ram = float(self.get_data(_oid_memAvailReal_))
            self.memory_used = 100.0 * (total_ram - avail_ram) / total_ram
        except Exception as e:
            print(e)
    
    def uptime(self):
        try:
            self.total_uptime = self.get_data(_oid_total_uptime)
        except Exception as e:
            print(e)
    
    def encrypt_data(self):
        combine = str(self.memory_used) + ':' + str(self.cpu_used) + ':' + str(self.total_uptime)
        self.key = Fernet.generate_key()
        cipher = Fernet(self.key)
        self.encrypt_data = cipher.encrypt(combine.encode("utf-8"))
        print(self.key.decode())
        print(self.encrypt_data.decode())