#Jennifer Salau, Institute of Animal Breeding and Husbandry, Kiel University
#Upload to Github in April 2019
#
#Use at own risk!

from recording import * #Cam2File_http, initialize_cam_object, available_cams, recording_inputs
from synchronization import * #SynchroObject, TimestampsConcatenated
from data_handling import data_handling
from multiprocessing import Pool
import numpy as np
#
import shutil
import time
import os
import logging
from recording import logfile_name

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
f_handler = logging.FileHandler(logfile_name.logfile_nme)
f_handler.setLevel(logging.INFO)
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)

# #####################################################################
# GENERAL RECORDING SETTINGS 
# ######################################################################
#
#----USER ACTION REQUIRED: specify your recording parameter---- Attention: not all combinations were tested, some might not be working, i.e. resolution '2688x1520' does not work with 'mp4' format
#
user = 'root' #the user name you use to address your IP cameras
resolution = '1920x1080'#one of the following: '2688x1520','1920x1080','1280x960','1280x720','1024x768','1024x576','800x600','640x480','640x360','352x240','320x240'
duration = '60'# in seconds, integer in single quotes
compression = '0' #integer between '0' to '100' in single quotes
fps = '1' #integer in single quotes
codec = 'x264'#'xvid'
file_ext = 'mp4'#'avi'
general_settings = [user, resolution, duration, compression, fps, codec, file_ext]
#######################################################################
# #threshold for synchronization
threshold = 0.01 #seconds
# two destinations to store and mirrow the recorded data, FULL PATHS; directory with recorded data will be copied/moved there
destination1 = "D:"
destination2 = "E:"
#######################################################################
#######################################################################
#
t_startmain = time.time()
if __name__ == '__main__':
# #######################################################################
# FIND AVAILABLE CAMERS IN THE SYSTEM
# ######################################################################
    t_available = time.time()
    available = available_cams.specify()
    print(f'\n\nTIME FOR SPECIFYING AVAILABLE CAMERAS {str(time.time() - t_available)}')
    logger.info(f'TIME FOR SPECIFYING AVAILABLE CAMERAS {str(time.time() - t_available)}')
#######################################################################
#
# ######################################################################
# PUT RECORDING INPUTS TOGETHER, USE CAMERA IPs AND PASSWORDS
# ######################################################################
    inputs = recording_inputs.concatenate(available, general_settings)
#######################################################################
#
# ######################################################################
# RECORDING
# ######################################################################
    t_recording = time.time()
    ts = time.strftime("%Y%m%d" + "-" + "%H%M%S", time.localtime(time.time()))
    if not os.path.exists("./" + ts[0:8]):
        print(f'Directory {ts[0:8]} NEEDS CREATION.')
        logger.info(f'Directory {ts[0:8]} NEEDS CREATION.')
        os.makedirs("./" + ts[0:8])
    else:
        print(f'Directory {ts[0:8]} already existing.')
        logger.info(f'Directory {ts[0:8]} already existing.')
#
    print(f'\n>>>Splitting up calculation in multiple processes for simultaneous recording with the available cameras.')
    logger.info(f'>>>Splitting up calculation in multiple processes for simultaneous recording with the available cameras.')
    with Pool(len(inputs)) as p:
        timestamp_files = p.map(initialize_cam_object.run, inputs)
    print(f'\n\nTIME FOR OPENING, RECORDING AND SHUTTING CAMERAS {time.time() - t_recording}')
    logger.info(f'TIME FOR OPENING, RECORDING AND SHUTTING CAMERAS {time.time() - t_recording}')
# ######################################################################
# SYNCHRONIZATION
# ######################################################################
    t_synchro = time.time()
    print(f'\n>>>Timestamps have been written in the following_files: {timestamp_files}')
    logger.info(f'>>>Timestamps have been written in the following_files: {timestamp_files}')
    print("\n>>>Synchronization: Generating tupels of images within a time window of " + str(threshold) + " seconds.")
    logger.info(f'>>>Synchronization: Generating tupels of images within a time window of {str(threshold)} seconds.')
    TC = TimestampsConcatenated.TimestampsConcatenated(timestamp_files)
    TC.concatenate_timestamplists()
    timestamp_array = TC.get_timestamp_array()
    S = SynchroObject.SynchroObject(threshold, timestamp_array)
    S.synchronize()
    synchronous_indices = S.get_synchronous_indices()
    np.savetxt(timestamp_files[0][0:10] + "/SynchronousIndices_" + timestamp_files[0][-10:-4] + ".csv", np.transpose(synchronous_indices), delimiter=',', fmt='%10.1e')
    print(f'\n\nTIME FOR SYNCHRONIZATION {time.time() - t_synchro}')
    logger.info(f'TIME FOR SYNCHRONIZATION {time.time() - t_synchro}')

#####################################################################
# MIRROR RECORDED DATA
#######################################################################
    t_datahandling = time.time()
    print("Starting data handling:")
    logger.info("Starting data handling:")
    data_handling.do(timestamp_files[0][0:10], destination1, destination2)
#
    print(f'\n\nTIME FOR DATA HANDLING{time.time() - t_datahandling }')
    logger.info(f'TIME FOR DATA HANDLING{time.time() - t_datahandling }')
    print("Final action: copying the log file...")
    logger.info("Final action: copying the log file...")
    shutil.copy(logfile_name.logfile_nme, destination1)
    shutil.copy(logfile_name.logfile_nme, destination2)
    print("\n---------------------------\n\nDONE! axis_device_control terminated gracefully.")
    logger.info("\n---------------------------\n\nDONE! axis_device_control terminated gracefully.")
