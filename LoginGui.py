#!/usr/bin/python
# encoding: utf-8
import os
import wx
from wx.lib.pubsub import pub as Publisher
import sys
import ssl
import FriendList
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
#import MySQLdb
import urllib2
import simplejson as json
#from gi.repository import Notify
import wx.lib.agw.toasterbox as TB
import thread
import gettext
import time
import locale
if locale.getdefaultlocale()[0] == 'zh_CN':
    gettext.install('messages', './locale', unicode=False)
    gettext.translation('messages', './locale', languages=['cn']).install(True)
class prpcrypt():
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC    
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0')
class LoginFrame(wx.Frame):
    def __init__(self, parent, id, title, size):
        wx.Frame.__init__(self, parent, id, title)
        self.SetSize(size)
        self.Center()
        self.passWordLabel = wx.StaticText(self, label = _("UserName"), pos = (30, 50), size = (120, 25))
        self.userNameLabel = wx.StaticText(self, label = _("Password"), pos = (30, 100), size = (120, 25))
        self.userName = wx.TextCtrl(self, pos = (100, 47), size = (150, 25),style=wx.TE_PROCESS_ENTER)
        self.passWord= wx.TextCtrl(self, pos = (100, 97), size = (150, 25),style=wx.TE_PASSWORD|wx.TE_PROCESS_ENTER)
        self.userName.Bind(wx.EVT_TEXT_ENTER,self.login_thread)
        self.passWord.Bind(wx.EVT_TEXT_ENTER,self.login_thread)
        self.loginButton = wx.Button(self, label = _('Login'), pos = (80, 145), size = (130, 30))
        self.loginButton.Bind(wx.EVT_BUTTON,self.login_thread)
        Publisher.subscribe(self.__Friend_list, 'list.show')
        self.Show()   
    def __Friend_list(self, info):
       #print 'Object', message.data, 'is added'
       self.Hide()
       frame = FriendList.MyFrame(None, id=-1, title=_("Friend List"),user=info.data,un=self.userName.GetValue())
       frame.Show(True)
    def login_thread(self,event):
            thread.start_new_thread(self.login, ())
            self.loginButton.Disable()
    def login(self):
            if not self.userName.GetValue():
                   wx.CallAfter(wx.MessageBox,_('Please enter the username'), _('Error'), 
                   wx.OK | wx.ICON_ERROR)
                   wx.CallAfter(self.loginButton.Enable)
            elif not self.passWord.GetValue():
                    wx.CallAfter(wx.MessageBox,_('Please enter the password'), _('Error'), 
                    wx.OK | wx.ICON_ERROR)     
                    wx.CallAfter(self.loginButton.Enable)      
            else:
              try:
                passwd = urllib2.urlopen("http://chat-tyl.coding.io/put_db.php?content=PASS&db=USER&where=NAME&where_t=" + self.userName.GetValue()).read()
              except urllib2.HTTPError,e:
                wx.CallAfter(wx.MessageBox,_('Unable to fetch data'),_('Error'), wx.OK | wx.ICON_ERROR)
                wx.CallAfter(self.loginButton.Enable)                                   
	      passwd0 = pc.decrypt(passwd)
              if self.passWord.GetValue()==passwd0:
                 print 'OK'
                 #try:
                        #cursor.execute("SELECT uncompress(Data) FROM friendlist WHERE name = '%s' LIMIT 1"%(self.userName.GetValue()))
                        #data = json.loads(cursor.fetchone()[0])
                        #cursor.close()
                        #conn.close()
                        #db.close()
                    #except IOError, e:      
                          #wx.CallAfter(wx.MessageBox,'Error %d: %s' % (e.args[0], e.args[1]),_('Try it again'), 
                          #wx.OK | wx.ICON_ERROR) 
                          #wx.CallAfter(self.loginButton.Enable)     
                    #urllib2.urlopen('http://chat-tyl.coding.io/user_log?info=User___'+self.userName.GetValue()+'___Login')
                    #time.sleep(0.1)
                    #wx.CallAfter(Notify.init,"Chat-TYL")
                    #bubble_notify = Notify.Notification.new (_("Information"),_("Login Successful"),"file://" + os.path.abspath(os.path.curdir) + "/Chat-TYL.ico")
                    #wx.CallAfter(bubble_notify.show) 
                    #wx.CallAfter(pub.sendMessage,'list.show', data)
              else:
                wx.CallAfter(wx.MessageBox,_('Your Password is wrong'), _('Try it again'), 
                wx.OK | wx.ICON_ERROR)
                     #wx.CallAfter(self.loginButton.Enable)    
if __name__ == '__main__':
    pc = prpcrypt('keyskeyskeyskeys')
    app = wx.App()
    LoginFrame(None, -1, title = _("Login"), size = (280, 210))
    app.MainLoop()
