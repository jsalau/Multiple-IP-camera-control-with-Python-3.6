#Jennifer Salau, Institute of Animal Breeding and Husbandry, Kiel University
#Upload to Github in April 2019
#
#Use at own risk!

import requests
from requests.auth import HTTPDigestAuth
from . import Cams
from recording import logfile_name
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
f_handler = logging.FileHandler(logfile_name.logfile_nme)
f_handler.setLevel(logging.INFO)
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)

def specify():
    available = {}
    print('\n>>>Starting specification of available cameras.')
    logger.info('>>>Starting specification of available cameras.')
    for k, ip_pwd in Cams.allCams.items():
        try:
            url = 'http://' + ip_pwd[0] + '/axis-cgi/mjpg/video.cgi'
            r = requests.get(url, auth=HTTPDigestAuth(r'root', ip_pwd[1]), stream=True)
            if r.status_code == requests.codes.ok:
                available[k] = True
                print(f'Camera {ip_pwd[0]} is available.')
                logger.info(f'Camera {ip_pwd[0]} is available.')
        except requests.exceptions.ConnectionError:
            available[k] = False
            print("requests.exceptions.ConnectionError: Camera " + ip_pwd[0] + " is NOT available!")
            logger.info(f'Exception occurred! requests.exceptions.ConnectionError: Camera {ip_pwd[0]} is NOT available!')
        except TimeoutError:
            available[k] = False
            print("TimeoutError: Camera " + ip_pwd[0] + " is NOT available!")
            logger.info(f'Exception occurred! TimeoutError: Camera {ip_pwd[0]} is NOT available!')
    return available
