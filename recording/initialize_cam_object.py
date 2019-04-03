#Jennifer Salau, Institute of Animal Breeding and Husbandry, Kiel University
#Upload to Github in April 2019
#
#Use at own risk!

from . import Cam2File_http
from recording import logfile_name
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
f_handler = logging.FileHandler(logfile_name.logfile_nme)
f_handler.setLevel(logging.INFO)
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)

def run(settings):  # camurl, passwd, user, resolution, duration, compression, fps, codec, filext):
    cam = Cam2File_http.Cam2File_http(settings[0], settings[1], settings[2], settings[3], settings[4], settings[5], settings[6],
                        settings[7], settings[8])
    print(f'Starting camera {settings[0]}')
    logger.info(f'Starting camera {settings[0]}')
    ts = cam.start_recording()
    print(ts)

    return(ts)
