from loguru import logger
import sys


logger.remove()
logger.add(
    sys.stdout,
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {extra[trace_id]} | {message}",
)


def get_logger(trace_id: str):
    return logger.bind(trace_id=trace_id)
