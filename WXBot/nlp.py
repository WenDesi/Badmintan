#!/usr/bin/env python
# coding: utf-8

class MMseg(object):
    def __init__(self,uuid,content):
        self.uuid = uuid
        self.content = content

class NLP(object):
    def __init__(self):
        self.msg_list = []
        self.XIAOBING = '小冰'

    def add_msg(self,uuid,content):
        mmseg = MMseg(uuid,content)
        self.msg_list.append(mmseg)

        return self.XIAOBING_UUID


    def add_msg_gzh(self,uuid,content,name):
        if name == self.XIAOBING:
            self.XIAOBING_UUID = uuid

            flag = False
            if len(self.msg_list) > 0:
                flag = True
                uuid = self.msg_list[0].uuid
                self.msg_list.pop(0)

            return flag,uuid,content
        else:
            return False,uuid,content

    def is_batminton_related(self,content):
        return False

