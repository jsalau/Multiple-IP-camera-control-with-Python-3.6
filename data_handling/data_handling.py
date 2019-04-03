#Jennifer Salau, Institute of Animal Breeding and Husbandry, Kiel University
#Upload to Github in April 2019
#
#Use at own risk!

import shutil
import os
from recording import logfile_name
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
f_handler = logging.FileHandler(logfile_name.logfile_nme)
f_handler.setLevel(logging.INFO)
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)


def do(datafolder, destination1, destination2):
     print("Mirroring and moving data:")
     logger.info("Mirroring and moving data:")

     if not os.path.exists(destination1 + "/" + datafolder):
          os.makedirs(destination1 + "/" + datafolder)
     if not os.path.exists(destination2 + "/" + datafolder):
          os.makedirs(destination2 + "/" + datafolder)
     for dirpath, dirnames, filenames in os.walk(datafolder):
          for file in filenames:
               shutil.copy(os.path.join(dirpath, file), destination1 + "/" + datafolder)
               logger.info(f'File {file} copied to {destination1 + "/" + datafolder}')
               shutil.move(os.path.join(dirpath, file), destination2 + "/" + datafolder)
               logger.info(f'File {file} copied to {destination2 + "/" + datafolder}')

     os.rmdir(datafolder)
     print(f'Removing recording directory {datafolder} from internal device.')
     logger.info(f'Removing recording directory {datafolder} from internal device.')
