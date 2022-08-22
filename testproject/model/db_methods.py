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