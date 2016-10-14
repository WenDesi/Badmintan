#!/usr/bin/env python
# coding: utf-8

from wxbot import *
import ConfigParser
import json

from nlp import NLP

class XiaobingWXBot(WXBot):
    def __init__(self):
        WXBot.__init__(self)

        self.tuling_key = ""
        self.robot_switch = True

        self.nlp = NLP()
        self.reply_list = ['温','司尚春','亲爱的']
        try:
            cf = ConfigParser.ConfigParser()
            cf.read('conf.ini')
            self.tuling_key = cf.get('main', 'key')
        except Exception:
            pass
        print 'tuling_key:', self.tuling_key

    def receive_msg(self, uid, content, name):
        print uid
        if self.is_batminton_related(content):
            pass
        else:
            if name in self.reply_list:
                xiaobing_uid = self.nlp.add_msg(uid,content)
                self.send_msg_by_uid(content,xiaobing_uid)

    def auto_reply(self, uid, content, name):
        reply_from_xiaobing,ouid,ocontent = self.nlp.add_msg_gzh(uid,content,name)

        if ouid == uid:
            return

        if reply_from_xiaobing:
            self.send_msg_by_uid(content,ouid)
        else:
            pass

    def is_batminton_related(self, msg):

        return self.nlp.is_batminton_related(msg)


    def auto_switch(self, msg):
        msg_data = msg['content']['data']
        stop_cmd = [u'退下', u'走开', u'关闭', u'关掉', u'休息', u'滚开']
        start_cmd = [u'出来', u'启动', u'工作']
        if self.robot_switch:
            for i in stop_cmd:
                if i == msg_data:
                    self.robot_switch = False
                    self.send_msg_by_uid(u'[Robot]' + u'机器人已关闭！', msg['to_user_id'])
        else:
            for i in start_cmd:
                if i == msg_data:
                    self.robot_switch = True
                    self.send_msg_by_uid(u'[Robot]' + u'机器人已开启！', msg['to_user_id'])

    def handle_msg_all(self, msg):
        if not self.robot_switch and msg['msg_type_id'] != 1:
            return
        if msg['msg_type_id'] == 1 and msg['content']['type'] == 0:  # reply to self
            self.auto_switch(msg)
        elif msg['msg_type_id'] == 4 and msg['content']['type'] == 0:  # text message from
            print msg['user']['name']
            self.receive_msg(msg['user']['id'], msg['content']['data'],msg['user']['name'])

        elif msg['msg_type_id'] == 5 and msg['content']['type'] == 0:  # text message from contact
            print msg['user']['name']
            self.auto_reply(msg['user']['id'], msg['content']['data'], msg['user']['name'])
            # self.send_msg_by_uid(self.auto_reply(msg['user']['id'], msg['content']['data']), msg['user']['id'])

        elif msg['msg_type_id'] == 3 and msg['content']['type'] == 0:  # group text message
            if 'detail' in msg['content']:
                my_names = self.get_group_member_name(self.my_account['UserName'], msg['user']['id'])
                if my_names is None:
                    my_names = {}
                if 'NickName' in self.my_account and self.my_account['NickName']:
                    my_names['nickname2'] = self.my_account['NickName']
                if 'RemarkName' in self.my_account and self.my_account['RemarkName']:
                    my_names['remark_name2'] = self.my_account['RemarkName']

                is_at_me = False
                for detail in msg['content']['detail']:
                    if detail['type'] == 'at':
                        for k in my_names:
                            if my_names[k] and my_names[k] == detail['value']:
                                is_at_me = True
                                break
                if is_at_me:
                    src_name = msg['content']['user']['name']
                    reply = 'to ' + src_name + ': '
                    if msg['content']['type'] == 0:  # text message
                        reply += self.xiaobing_auto_reply(msg['content']['user']['id'], msg['content']['desc'])
                    else:
                        reply += u"对不起，只认字，其他杂七杂八的我都不认识，,,Ծ‸Ծ,,"
                    self.send_msg_by_uid(reply, msg['user']['id'])


def main():
    bot = XiaobingWXBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'png'

    bot.run()


if __name__ == '__main__':
    main()

