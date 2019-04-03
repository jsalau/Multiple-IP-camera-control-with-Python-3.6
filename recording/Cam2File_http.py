#Jennifer Salau, Institute of Animal Breeding and Husbandry, Kiel University
#Upload to Github in April 2019
#
#Use at own risk!

import cv2
import time
from recording import logfile_name
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
f_handler = logging.FileHandler(logfile_name.logfile_nme)
f_handler.setLevel(logging.INFO)
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)

class Cam2File_http():

    def __init__(self, camurl, passwd, user,
                 resolution, duration, compression, fps,
                 codec, file_ext):
        self.__camurl = camurl
        self.__passwd = passwd
        self.__user = user
        self._resolution = resolution
        self._duration = duration
        self._compression = compression
        self._fps = fps
        self._codec = codec
        self._file_ext = file_ext
        # log parameter setting and print it to console:
        logger.info(f'Camera {camurl} initialized: Resolution: {resolution}, frames per second: {fps}, compression: {compression}')
        print("\n\nCamera " + camurl + " initialized.")
        print("\tResolution: " + resolution)
        print("\tFrames per second: " + fps)
        print("\tCompression: " + compression)

    def transform_resolution(self):
        res_nos = self._resolution.split("x")
        return [int(res_nos[0]), int(res_nos[1])]

    def url2camname(self):
        splitted_url = self.__camurl.split(".")[-1]
        if len(splitted_url) == 1:
            splitted_url = "0" + splitted_url
        return "CAU1071-13" + splitted_url

    def build_filename(self):
        cam_name = Cam2File_http.url2camname(self)
        ts = time.strftime("%Y%m%d" + "-" + "%H%M%S", time.localtime(time.time()))
        filename = "./" + ts[0:8] + "/Recording_" + cam_name + "_" + ts \
                   + "_Resolution" + self._resolution + "_fps" + self._fps \
                   + "_Comp" + self._compression + "_" + self._codec + "." + self._file_ext

        return cam_name, filename, ts

    def vcap_input(self):
        return "http://" + self.__user + ":" + self.__passwd + "@" \
               + self.__camurl + "/axis-cgi/mjpg/video.cgi?" + "resolution=" \
               + self._resolution + "&duration=" + self._duration \
               + "&compression=" + self._compression + "&camera=1&fps=" + self._fps

    def start_recording(self):
        res = Cam2File_http.transform_resolution(self)
        cam_name, filename, ts = Cam2File_http.build_filename(self)
        #
        logger.info(f'Setting up VideoWriter object for camera {self.__camurl}!')
        print(f'\nSetting up VideoWriter object for camera {self.__camurl}!')
        fourcc = cv2.VideoWriter_fourcc(*self._codec)
        out = cv2.VideoWriter(filename,
                              fourcc,
                              float(self._fps),
                              (res[0], res[1])
                              )
        #
        print(f'Writing to file: {filename}')
        logger.info(f'Writing to file: {filename}')
        print(f'Starting recording with camera {self.__camurl}!')
        logger.info(f'Starting recording with camera {self.__camurl}!')
        vcap_id = Cam2File_http.vcap_input(self)
        vcap = cv2.VideoCapture(vcap_id)
        print(f'Camera has been opened: {vcap.isOpened()}')
        logger.info(f'Camera has been opened: {vcap.isOpened()}')
        start_time = time.time()
        timestamp_file = open(r"./" + ts[0:8] + "/Timestamps_" + cam_name + "_" + ts + ".txt", 'a')
        timestamp_file.write(str(start_time) + "\n")
        #
        ret = True
        while vcap.isOpened() and ret:
            curr_time = start_time + 1 / 1000 * vcap.get(cv2.CAP_PROP_POS_MSEC)
            timestamp_file.write(str(curr_time) + "\n")
            ret, frame = vcap.read()
            if ret:
                out.write(frame)
            else:
                print(f'Camera {self.__camurl} was closed!')
                logger.info(f'Camera {self.__camurl} was closed!')
        timestamp_file.close()
        print('\n-------------------Recording was finished.-------------------')
        logger.info('\n-------------------Recording was finished.-------------------')

        return r"./" + ts[0:8] + "/Timestamps_" + cam_name + "_" + ts + ".txt"