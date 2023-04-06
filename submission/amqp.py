import pika
import logging
import json
from submission.task.models import Task
from submission_lib.manage import wait_job
from server.settings import AMQP_CONFIG

logger = logging.getLogger(__name__)

amqp_con = None  # Not initialized connection

AMQP_HOST = AMQP_CONFIG.get("HOST")
AMQP_PORT = int(AMQP_CONFIG.get("PORT", 5672))

if AMQP_HOST:
    if AMQP_CONFIG.get("USER") and AMQP_CONFIG.get("PASSWORD"):
        credentials = pika.PlainCredentials(AMQP_CONFIG.get("USER"), AMQP_CONFIG.get("PASSWORD"))
        con_params = pika.ConnectionParameters(host=AMQP_HOST, port=AMQP_PORT, credentials=credentials)
    else:
        con_params = pika.ConnectionParameters(host=AMQP_HOST, port=AMQP_PORT)
    amqp_con = pika.BlockingConnection(con_params)
else:
    logger.info("No AMQP host provided. AMQP client not initialized.")


def basic_publish(exchange, route, message):
    channel = amqp_con.channel()
    channel.basic_publish(exchange=exchange, routing_key=route, body=message)
    channel.close()

def do_wait(task: Task, exchange, route, timeout = 60):
    timeout_flag = False
    job_info = {}
    logger.info(f"Init wait for task {str(task.uuid)}")
    try:
        job_info = wait_job(task._drm_job_id, timeout=timeout)._asdict()       
    except:
        logger.error(f"Timeout wait for task {str(task.uuid)}")
        timeout_flag = True
    logger.info(f"End wait for task {str(task.uuid)}")

    message = json.dumps({
        "task": str(task.uuid),
        "timeout": timeout_flag,
        "job_info": {
            "hasExited": job_info.get("hasExited", False),
            "wasAborted": job_info.get("wasAborted", False),
            "exitStatus": job_info.get("exitStatus", -1)
        }
    })

    basic_publish(exchange, route, message)