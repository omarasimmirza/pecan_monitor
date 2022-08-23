from .model.db_methods import insert_to_table
from .model.db_model import Stats
from .libserver import SystemCheck

# def parse_xml(filename):
#     try:
#         list_of_machines = []
#         tree = et.parse(filename)
#         root = tree.getroot()
#         for child in root:
#             machine = SystemCheck()
#             machine.ip = child.attrib.get("ip")
#             machine.port = int(child.attrib.get("port"))
#             machine.user = child.attrib.get("username")
#             machine.password = child.attrib.get("password")
#             machine.mail = child.attrib.get("mail")
#             if len(child) > 0:
#                 alert_dict = dict()
#                 for alert_child in child:
#                     alert_type = alert_child.attrib.get("type")
#                     alert_dict[alert_type] = alert_child.attrib.get("limit")
#                 machine.alert.append(alert_dict)
#             list_of_machines.append(machine)
#     except Exception:
#         print("Error: XML file not found.")
#     for items in list_of_machines:
#         print(items.ip)
#     return list_of_machines
def set_up(machine_dict):
    try:
        list_of_machines = []
        for key, val in machine_dict.items():
            # for key2, val2 in val.items():
            machine = SystemCheck()
            machine.ip = val['ip']
            machine.port = int(val['port'])
            machine.user = val['username']
            machine.password = val['password']
            machine.mail = val['mail']
            if 'alert' in val:
                for index, alert in val['alert'].items():
                    machine.alert.append(alert)
            list_of_machines.append(machine)
    except Exception as e:
        print(e)

    for checker in list_of_machines:
        data = checker.ssh_connect()
        
        for items in data:
            print(items)
            
        print(checker.alert)

        add_this = Stats(
            ip=checker.ip,
            port=checker.port,
            username=checker.user,
            mail=checker.mail,
            cpu_uptime=data[2],
            cpu_usage=data[1],
            memory_usage=data[0]
        )

        insert_to_table(add_this)
        checker.email_user()