print('start')
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from connection import Connection
from job import Job
from util import Util

utility = Util()
client = utility.create_slack_client()
bot_id = utility.get_bot_id()

connection = Connection(r'/home/gsl-ggn-lt-55/qa-bot/database.db')
engine = connection.get_engine()

def traverse_table():
    print("CHECKING")
    Session = sessionmaker(bind=engine)
    session = Session()

    jobs = ''

    try:
        jobs = session.query(Job).all()
    except Exception as e:
        print(str(e))

    print("jobs")
    current_time = datetime.now()
    current_time_formatted = current_time.strftime("%H:%M")
    print(current_time_formatted, "HERE")

    for job in jobs:
        print("LOOPING")
        channel_id = job.channelid
        print(channel_id, job.next_message_time, job.next_message_time_string)
        

        if job.next_message_time_string == current_time_formatted:

            status = utility.send_message(client, channel_id, 'HOURLY MESSAGE')

            if status:
                print('SENT')
            else:
                print('FAILED')

            next_hour = current_time + timedelta(hours=1)  
            next_hour_formatted = next_hour.strftime("%H:%M")

            job.next_message_time = next_hour 
            job.next_message_time_string = next_hour_formatted
            session.commit()

    session.close()

traverse_table()
print("HERE")