import time
import random

from celery import shared_task


@shared_task
def analyze_commits(url):
    # Sleep for a random time between 5 and 15 seconds
    sleep_time = random.randint(5, 15)
    time.sleep(sleep_time)
    # Add your actual implementation here, if needed
    return {"url": url, "sleep_time": sleep_time}
