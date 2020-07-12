import logging
import requests

def log_track(endpoint='/'):

    ## Get an instance of a logger
    logger = logging.getLogger(__name__)

    resp_1, resp_2 = requests.get('https://www.cloudflare.com/cdn-cgi/trace'), requests.get('http://www.geoplugin.net/json.gp')
    resp_1 = resp_1.text.replace('\n', '')
    resp_2 = resp_2.text.replace('\n', '')
    logger.info(
        f"Tracking: [Data_1={resp_1}] [Data_2={resp_2}] [Endpoint={endpoint}]"
    )
    return True