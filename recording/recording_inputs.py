#Jennifer Salau, Institute of Animal Breeding and Husbandry, Kiel University
#Upload to Github in April 2019
#
#Use at own risk!

from . import Cams


def concatenate(available, general_settings):
    print("\n>>>Putting together the input parameters for the camera recording objects.")
    inputs = []
    for k in Cams.allCams.keys():
        if available[k]:
            inputs.append(Cams.allCams[k] + general_settings)
    return inputs
