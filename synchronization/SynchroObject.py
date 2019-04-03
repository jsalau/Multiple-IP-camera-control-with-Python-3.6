#Jennifer Salau, Institute of Animal Breeding and Husbandry, Kiel University
#Upload to Github in April 2019
#
#Use at own risk!

import numpy as np
from recording import logfile_name
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
f_handler = logging.FileHandler(logfile_name.logfile_nme)
f_handler.setLevel(logging.INFO)
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)


class SynchroObject():

    def __init__(self, threshold, timestamp_array):
        self.threshold = threshold
        self.timestamp_array = timestamp_array
        self.no_cams = len(timestamp_array)
        self.__offsets = [0 for x in range(0, self.no_cams - 1)]
        self.__order = []
        self.__ref_cam = -1
        self.__synchronous_indices = []

    def update_order(self, t):
        # arrange all timestamps of time t in the second column of an array associated with the consecutive camera indices in the first column
        data = np.array([[i, self.timestamp_array[i][t]] for i in range(0, self.no_cams)])
        # sort the array by the second column in descending order
        data = data[np.argsort(data[:, 1])][::-1]
        # address the first column (camera indices sorted by the timestamps at time t)
        self.__order = [int(row[0]) for row in data]
        print(f'    SynchroObject: Updating camera order:\nrelevant timestamps (all cameras) {[row[1] for row in data]}; order {self.__order}')
        self.__ref_cam = self.__order[0]
        logger.info(f'SynchroObject: Updating camera order:\nrelevant timestamps (all cameras) {[row[1] for row in data]}; order {self.__order}')


    def get_order(self):
        return self.__order

    def update_offsets(self, t):
        r = self.timestamp_array[self.__ref_cam][t]
        for i in range(1, self.no_cams):
            comp_cam_data = self.timestamp_array[self.__order[i]]
            x = [j for j in range(0, len(comp_cam_data)) if comp_cam_data[j] >= r]
            if abs(comp_cam_data[x[0]] - r) > abs(comp_cam_data[x[0] - 1] - r):
                self.__offsets[i - 1] = int(x[0] - 1)
            else:
                self.__offsets[i - 1] = int(x[0])
        print(f'    Current index-offsets compared to reference camera: {self.__offsets}')
        logger.info(f'Current index-offsets compared to reference camera: {self.__offsets}')

    def get_offset(self):
            return self.__offsets

    def store_indices(self, indices):
        data = np.hstack([np.array(indices).reshape(len(self.__order), 1), np.array(self.__order).reshape(len(self.__order), 1)])
        #        print("\nstore_indices, revert order of synchronous indices:")
        indices = data[np.argsort(data[:, 1])][:, 0]
        if len(self.__synchronous_indices) == 0:
            for i in range(0, self.no_cams):
                self.__synchronous_indices.append([indices[i]])
        else:
            for i in range(0, self.no_cams):
                self.__synchronous_indices[i].append(indices[i])

    def compare_timestamps(self, index):
        ref_cam_data = self.timestamp_array[self.__order[0]]
        dist = ref_cam_data[index] - np.array(self.timestamp_array)[self.__order[1:], index + np.array(self.__offsets)]
        #
        return [dist, [index] + list(index + np.array(self.__offsets))]

    def neighbouring_timestamps(self, index):
        ref_cam_data = self.timestamp_array[self.__order[0]]
        # ATTENTION: We allow that an image is skipped with considering d_plus!
        d_plus = ref_cam_data[index] - np.array(self.timestamp_array)[
            self.__order[1:], index + 1 + np.array(self.__offsets)]
        # ATTENTION: We allow that an image is used twice with considering d_minus!
        d_minus = np.array([])
        if index > 1:
            d_minus = ref_cam_data[index] - np.array(self.timestamp_array)[
                self.__order[1:], index - 1 + np.array(self.__offsets)]
        return np.hstack([d_plus, d_minus])

    def update_offsets_using_neighbours(self, min_indices):
        loc2 = [i for i in range(0, np.size(min_indices)) if min_indices[i] == 2]
        min_indices[loc2] = -1
        self.__offsets = list(np.array(self.__offsets) + min_indices)
        

    def synchronize(self):
        SynchroObject.update_order(self, 0)
        print(f'    ref_cam: {self.__ref_cam}')
        logger.info(f'ref_cam: {self.__ref_cam}')
        SynchroObject.update_offsets(self, 0)
        for index in range(0, len(self.timestamp_array[0])):
            try:
                dist, indices = SynchroObject.compare_timestamps(self, index)
                if all(dist <= self.threshold):
                    SynchroObject.store_indices(self, indices)
                else:
                    print("     Trying neighbouring images instead.\nD = [dist;d+;d-]:")
                    D = np.hstack([dist, SynchroObject.neighbouring_timestamps(self, index)])
                    D = abs(D.reshape(self.no_cams - 1, int(np.size(D) / (self.no_cams - 1))))
                    logger.info(f'Trying neighbouring images instead.\nD = [dist;d+;d-]: {D}')
                    if all(D.min(axis=0) < self.threshold):
                        SynchroObject.update_offsets_using_neighbours(self, D.argmin(axis=0))
                        SynchroObject.store_indices(self, [index] + list(index + np.array(self.__offsets)))
                        # make sure that ref_cam is stil valid
                        if any(self.__offsets < 0):
                            SynchroObject.update_order(self, index + 1)
                            print(f'    ref_cam: {self.__ref_cam}')
                            logger.info(f'ref_cam: {self.__ref_cam}')
                            SynchroObject.update_offsets(self, index + 1)
                        else:
                            SynchroObject.update_order(self, index)
                            print(f'    ref_cam: {self.__ref_cam}')
                            logger.info(f'ref_cam: {self.__ref_cam}')
                            SynchroObject.update_offsets(self, 0)
                            dist, indices = SynchroObject.compare_timestamps(self, index)
                            if all(dist <= self.threshold):
                                SynchroObject.store_indices(self, indices)
                            else:
                                print("     Trying neighbouring images instead.\nD = [dist;d+;d-]:")
                                D = np.hstack([dist, SynchroObject.neighbouring_timestamps(self, index)])
                                D = abs(D.reshape(self.no_cams - 1, int(np.size(D) / (self.no_cams - 1))))
                                print(D)
                                logger.info(f'Trying neighbouring images instead.\nD = [dist;d+;d-]: {D}')
                                if all(D.min(axis=0) < self.threshold):
                                    SynchroObject.update_offsets_using_neighbours(self, D.argmin(axis=0))
                                    SynchroObject.store_indices(self, [index] + list(index + np.array(self.__offsets)))
                                else:
                                    print(f'    SynchroObject: Problem with index {index}! No synchronization possible here.')
                                    logger.info(f'SynchroObject: Problem with index {index}! No synchronization possible here.')
                                    continue
            except IndexError:
                print(f'    SynchroObject: Finishing synchronization at image {index}')
                logger.info(f'SynchroObject: Finishing synchronization at image {index}')
                return


    def get_synchronous_indices(self):
            return self.__synchronous_indices
