#Jennifer Salau, Institute of Animal Breeding and Husbandry, Kiel University
#Upload to Github in April 2019
#
#Use at own risk!

class TimestampsConcatenated():

    def __init__(self, timestamp_files):
        self.timestamp_files = timestamp_files
        self.__timestamp_dictionary = {}
        self.max_len = 0
        self.__timestamp_array = []

    def read_timestamp_files(self):
        for f in self.timestamp_files:
            content = []  
            with open(str(f), 'r') as file:
                for line in file:
                    content.append(float(line.strip()))
                    self.__timestamp_dictionary[f] = content

    def get_timestamp_dictionary(self):
        return self.__timestamp_dictionary

    def max_len(self):
        D = list(self.__timestamp_dictionary.keys())
        for k in D:
            if len(self.__timestamp_dictionary[k]) > self.max_len:
                self.max_len = len(self.__timestamp_dictionary[k])
                print("     max_len:")
                print(self.max_len)

    def concatenate_timestamplists(self):
        TimestampsConcatenated.read_timestamp_files(self)
        TimestampsConcatenated.max_len(self)
        D = list(self.__timestamp_dictionary.keys())
        for k in D:
            ts = self.__timestamp_dictionary[k]
            while len(ts) < self.max_len:
                ts.append(-1)

            self.__timestamp_array.append(ts)

    def get_timestamp_array(self):
        return self.__timestamp_array
