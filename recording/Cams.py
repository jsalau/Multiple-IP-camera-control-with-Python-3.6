#Jennifer Salau, Institute of Animal Breeding and Husbandry, Kiel University
#Upload to Github in April 2019
#
#Use at own risk!

from recording import logfile_name
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
f_handler = logging.FileHandler(logfile_name.logfile_nme)
f_handler.setLevel(logging.INFO)
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)
###############################
# allCams needs to be a dictionary with one entry per camera: 'indiv_camkey': [r'cam_ip', 'cam_password'].  'indiv_camkey' can be anything, but we recommend something specific for exactly the camera you are referring to her, for example the MAC address. Each camera needs to be assigned an IP address in your network ('cam_ip') and should be password protected ('cam_password') for privacy and data savety reasons.
#
#see example below:
###############################
'''
allCams = {'AXXX11YY888B': [r'333.444.5.66', 'very_s3cuRe_Pw%'],
		....
		}
'''
print(f'\nList of cameras to search for: {[x[0] for x in allCams.values()]}')
logger.info(f'List of cameras to search for: {[x[0] for x in allCams.values()]}')