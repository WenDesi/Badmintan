# coding: utf-8

class Yard(object):
    def __init__(self,name):
        self.__name = name
        self.__time_dict = {}

    def add_time(self,time,flag,yard_id,time_id):
        self.__time_dict[time] = (flag,yard_id,time_id)

    def is_value(self,start_time,end_time):
        start_time = int(start_time[:2])
        end_time = int(end_time[:2])

        time = start_time

        ids = []
        while time < end_time:
            print str(time)+':00'
            tmp = self.__time_dict[str(time)+':00']

            flag = tmp[0]
            yard_id = tmp[1]
            time_id = tmp[2]

            if flag != 0:
                return False,[]

            ids.append([yard_id,time_id])
            time += 1

        return True,ids
