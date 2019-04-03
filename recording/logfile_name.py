#Jennifer Salau, Institute of Animal Breeding and Husbandry, Kiel University
#Upload to Github in April 2019
#
#Use at own risk!

import time

ts = time.strftime("%Y%m%d" + "-" + "%H%M%S", time.localtime(time.time()))
logfile_nme = f'Logfile_AxisDeviceControl_{ts[0:8]}.log'