from .model.db_methods import insert_to_table
from .model.db_model import Stats
from .libserver import SystemCheck

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
            if (len(val['alert']) != 0):
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
        if(len(checker.alert) != 0):
            checker.email_user()