from .db_model import Stats
from .db_connection import session

def insert_to_table(info:Stats):
    try:
        existing_user = session.query(
                    session.query(Stats).filter(Stats.ip == info.ip).exists()
                ).scalar()
        if not existing_user:
            session.add(info)
            session.commit()
            print(f"Created new record for {info.ip}")
        else:
            print(existing_user)
            session.query(Stats).filter_by(ip=info.ip).\
            update(
                    {
                        'cpu_uptime': info.cpu_uptime, 
                        'cpu_usage': info.cpu_usage, 
                        'memory_usage': info.memory_usage
                    }, 
                    synchronize_session="fetch"
                )
            session.commit()
            print(f"Info for {info.ip} updated.")
    except Exception as e:
        print(e)

def get_all():
    machine_list = []
    try:
        for machines in session.query(Stats).all():
            machine_list.append(machines)   
        return machine_list
    except Exception as e:
        print(e)

def get_one(ip):
    return session.query(Stats).filter(Stats.ip == ip).all()

    machine = []
    try:
        machine.append(session.query(Stats).filter(Stats.ip == ip).all())
        return machine
    except Exception as e:
        print(e)

def delete(ip):
    done = session.query(Stats).filter(Stats.ip == ip).delete()
    session.commit()
    if done:
        return True
    return False

def update(data, ip):
    done = session.query(Stats).filter(Stats.ip == ip)\
        .update(
            {
                # 'port': int(data['port']),
                # 'username': data['username'],
                'mail': data['mail']
                # 'cpu_uptime': float(data['cpu_uptime']), 
                # 'cpu_usage': float(data['cpu_usage']), 
                # 'memory_usage': float(data['memory_usage'])
            },
            synchronize_session='fetch'
        )
    session.commit()
    if done:
        return True
    return False