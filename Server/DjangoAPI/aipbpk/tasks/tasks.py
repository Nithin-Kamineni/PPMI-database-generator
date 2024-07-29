from celery import shared_task
import time

@shared_task
def long_running_task(data):
    try:
        # Log the received data
        # logger.info(f"Starting long-running task with data: {data}")
        
        # Simulate a long-running task
        time.sleep(30)  # 5 minutes
        
        # Log completion
        # logger.info("Task completed successfully.")
        
        return f'Task completed with data: {data}'
    except Exception as e:
        # logger.error(f"An error occurred: {e}")
        raise