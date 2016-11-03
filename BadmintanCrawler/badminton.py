#!/usr/bin/python
# coding: utf-8

import HTMLParser
import urlparse
import urllib
import urllib2
import cookielib
import string
import re
import json
import time

from yard import Yard


class Badminton(object):

    def __init__(self):
        self.host = 'http://219.223.222.202:8080/'
        self.login_url = self.host + '/admin/clientuser/login.do'
        self.court_info_url = self.host + '/admin/appointmenrecord/initByDate.do'
        self.book_court_url = self.host + '/admin/appointmenrecord/addSave.do'


        self.cj = cookielib.LWPCookieJar()
        cookie_support = urllib2.HTTPCookieProcessor(self.cj)
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)

        self.headers= {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1'}


        self.__room1 = Yard('场地一')
        self.__room2 = Yard('场地二')
        self.__room3 = Yard('场地三')

    def login(self):
        postData = {
                    'loginName' : '1501213990',
                    'password' : '303512',
                    }

        postData = urllib.urlencode(postData)

        request = urllib2.Request(self.login_url, postData, self.headers)
        response = urllib2.urlopen(request)
        json_data = response.read()

        s = json.loads(json_data)

        self.st = s['st']
        self.token = s['token']
        self.singnature = s['singnature']


    def check_court_info(self,date):
        # date = time.strftime("%Y-%m-%d", time.localtime())

        postData = {
                    'appDate' : date,
                    'st' : self.st,
                    'token' : self.token,
                    'singnature' : self.singnature,
                    }

        postData = urllib.urlencode(postData)

        request = urllib2.Request(self.court_info_url, postData, self.headers)
        response = urllib2.urlopen(request)
        json_data = response.read()


        s = json.loads(json_data)

        for rooms in s['data']:
            print '%s %s to %s ' % (date,rooms['startTime'],rooms['endTime'])

            start_time = rooms['startTime']
            # if rooms['startTime'] != '22:00' and rooms['startTime'] != '23:00':
            #     continue

            for room in rooms['listRoom']:
                yard = None
                if room['name'] == u'场地一':
                    yard = self.__room1
                elif room['name'] == u'场地二':
                    yard = self.__room2
                else:
                    yard = self.__room3

                yard.add_time(start_time,room['flag'],room['id'],rooms['id'])

                # if room['flag'] == 0:
                #     print '%s is free now!' % room['name']
                #
                #     roomId = room['id']
                #     timeIds = rooms['id']
                #
                #     self.book_court(roomId,timeIds,date)
                #     # return


    def book(self,date,start_time,end_time):
        room1_ok,ids1 = self.__room1.is_value(start_time,end_time)
        room2_ok,ids2 = self.__room2.is_value(start_time,end_time)
        room3_ok,ids3 = self.__room3.is_value(start_time,end_time)

        if room1_ok:
            for roomID,timeID in ids1:
                self.book_court(roomID,timeID,date)
            return 1

        if room2_ok:
            for roomID,timeID in ids2:
                self.book_court(roomID,timeID,date)
            return 2

        if room3_ok:
            for roomID,timeID in ids3:
                self.book_court(roomID,timeID,date)
            return 3

        return 0



    def book_court(self,roomId,timeIds,date):
        postData = {
                    'appDate' : date,
                    'roomId' : roomId,
                    'timeIds[0]' : timeIds,
                    'st' : self.st,
                    'token' : self.token,
                    'singnature' : self.singnature,
                    }

        postData = urllib.urlencode(postData)

        request = urllib2.Request(self.book_court_url, postData, self.headers)
        response = urllib2.urlopen(request)
        json_data = response.read()

        print json_data



if __name__ == '__main__':

    date = "2016-11-05"

    bt = Badminton()
    bt.login()
    bt.check_court_info(date)
    print bt.book(date,'15:00','17:00')
