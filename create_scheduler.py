from shared_queue import get_shared_queue
import schedule
import threading
import time

def send_hourly_message(channel_id):
    print(f"Sending hourly message to channel {channel_id}.")

channel_jobs = {}

def schedule_hourly_messages(channel_id, join_time):
    cron_minute = int((join_time - int(join_time)) * 60)
    cron_hour = int(join_time)
    cron_schedule = f"{cron_minute} {cron_hour} * * *"

    schedule.every().hour.at(f":{cron_minute}").do(send_hourly_message, channel_id=channel_id)

    channel_jobs[channel_id] = cron_schedule

def handle_channel_join(channel_id, join_time):
    if channel_id in channel_jobs:
        print(f"Hourly messages for channel {channel_id} are already scheduled.")
    else:
        schedule_hourly_messages(channel_id, join_time)
        print(f"Scheduled hourly messages for channel {channel_id}.")

def run_scheduler(request_queue):
    while True:
        schedule.run_pending()
        while not request_queue.empty():
            request = request_queue.get()
            handle_channel_join(request['channel_id'], request['time'])

request_queue = get_shared_queue()

scheduler_thread = threading.Thread(target=run_scheduler, args=(request_queue,))
scheduler_thread.start()
