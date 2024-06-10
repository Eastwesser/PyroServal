import logging
import re


async def handle_triggers(text):
    logging.info(f"Checking triggers for text: {text}")
    if re.search(r'прекрасно|ожидать', text, re.IGNORECASE):
        if 'прекрасно' in text.lower():
            logging.info(f"Trigger word 'прекрасно' found in text: {text}")
            return 'finished'
        elif 'ожидать' in text.lower():
            logging.info(f"Trigger word 'ожидать' found in text: {text}")
            return 'waiting'
    logging.info(f"No trigger words found in text: {text}")
    return False
