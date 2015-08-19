#!/usr/bin/python
# encoding: utf-8
import os
import wx
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub
import sys
import ssl
import FriendList
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
#import MySQLdb
import urllib2
import urllib
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
    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        length = 32
        count = len(text)
        add = length - (count % length)
        text = text + ('\0' * add)
        self.ciphertext = cryptor.encrypt(text)
        return b2a_hex(self.ciphertext)

class LoginFrame(wx.Frame):
    def __init__(self, parent, id, title, size):
        wx.Frame.__init__(self, parent, id, title)
        self.SetSize(size)
        self.Center()
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ))
        self.passWordLabel = wx.StaticText(self, label = _("UserName"), pos = (30, 40), size = (120, 25))
        self.userNameLabel = wx.StaticText(self, label = _("Password"), pos = (30, 90), size = (120, 25))
        self.userName = wx.TextCtrl(self, pos = (85, 37), size = (150, 25),style=wx.TE_PROCESS_ENTER)
        self.passWord= wx.TextCtrl(self, pos = (85, 87), size = (150, 25),style=wx.TE_PASSWORD|wx.TE_PROCESS_ENTER)
        self.userName.Bind(wx.EVT_TEXT_ENTER,self.login_thread)
        self.passWord.Bind(wx.EVT_TEXT_ENTER,self.login_thread)
        self.cb = wx.CheckBox(self, pos=(30,120) ,label="I am new user", size=(120,25))
        self.loginButton = wx.Button(self, label = _('Login'), pos = (80, 145), size = (130, 30))
        self.loginButton.Bind(wx.EVT_BUTTON,self.login_thread)
        pub.subscribe(self.__Friend_list, 'list.show')
        self.Show()   
    def __Friend_list(self, data):
       #print 'Object', message.data, 'is added'
       #print data
       self.Hide()
       time.sleep(0.1)
       frame = FriendList.MyFrame(None, id=-1, title=_("Friend List"),user=data,un=self.userName.GetValue())
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
           if self.cb.IsChecked()==False:
              try:
                passwd = urllib2.urlopen("http://chat-tyl.coding.io/put_db.php?content=PASS&db=USER&where=NAME&where_a==&where_t=" + self.userName.GetValue()).read()
              except urllib2.HTTPError,e:
                wx.CallAfter(wx.MessageBox,_('Unable to fetch data'),_('Error'), wx.OK | wx.ICON_ERROR)
                wx.CallAfter(self.loginButton.Enable)                                   
	      passwd0 = pc.decrypt(passwd)
              if self.passWord.GetValue()==passwd0: 
                 #urllib2.urlopen('http://chat-tyl.coding.io/user_log?info=User___'+self.userName.GetValue()+'___Login')
                 try:
                   data = urllib2.urlopen("http://chat-tyl.coding.io/put_db.php?content=FRIEND&db=USER&where=NAME&where_a==&where_t=" + self.userName.GetValue()).read()
                 except urllib2.HTTPError,e:
                   wx.CallAfter(wx.MessageBox,_('Unable to fetch data'),_('Error'), wx.OK | wx.ICON_ERROR)
                   wx.CallAfter(self.loginButton.Enable)
                 time.sleep(0.1)
                 wx.CallAfter(pub.sendMessage,'list.show', data=json.loads(data))
              else:
                wx.CallAfter(wx.MessageBox,_('Your Password is wrong'), _('Try it again'), 
                wx.OK | wx.ICON_ERROR)
                wx.CallAfter(self.loginButton.Enable) 
           else:
             try:
               cont = urllib2.urlopen("http://chat-tyl.coding.io/put_db.php?content=PASS&db=USER&where=NAME&where_a==&where_t=" + self.userName.GetValue()).read()
             except urllib2.HTTPError,e:
               wx.CallAfter(wx.MessageBox,_('Check Your NetWork,and try it again'),_('Error'), wx.OK | wx.ICON_ERROR)
               wx.CallAfter(self.loginButton.Enable)
             if not cont:   
               try:
                req = urllib2.Request("http://chat-tyl.coding.io/in_db.php")
                data = urllib.urlencode({'db':'USER','name':self.userName.GetValue(),'pass':pc.encrypt(self.passWord.GetValue()),'friend':"{\"item\":[\"friend\"],\"friend\":[\"tyl\",\"Test\"]}",'avatar':'default','info':"{\"name\":[\"" + self.userName.GetValue() + "\"]}"})
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor()) 
                opener.open(req, data).read()  
               except urllib2.HTTPError,e:
                 wx.CallAfter(wx.MessageBox,_("We can't register,check your network and try it again"),_('Error'), wx.OK | wx.ICON_ERROR)
                 wx.CallAfter(self.loginButton.Enable)    
               wx.CallAfter(wx.MessageBox,_("Register Successful"),_('Information'), wx.OK | wx.ICON_INFORMATION)
               wx.CallAfter(self.loginButton.Enable)
             else:
               wx.CallAfter(wx.MessageBox,_('You already registered'),_('Error'), wx.OK | wx.ICON_ERROR)
               wx.CallAfter(self.loginButton.Enable)       
if __name__ == '__main__':
    pc = prpcrypt('keyskeyskeyskeys')
    app = wx.App()
    LoginFrame(None, -1, title = _("Login"), size = (280, 210))
    app.MainLoop()
