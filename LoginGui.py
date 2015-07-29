#!/usr/bin/python
# encoding: utf-8
import os
import wx
import sys
import ssl
import FriendList
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import MySQLdb
import simplejson as json
from gi.repository import Notify
import gettext
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
        self.userName = wx.TextCtrl(self, pos = (100, 47), size = (150, 25))
        self.passWord= wx.TextCtrl(self, pos = (100, 97), size = (150, 25),style=wx.TE_PASSWORD)
        self.loginButton = wx.Button(self, label = _('Login'), pos = (80, 145), size = (130, 30))
        self.loginButton.Bind(wx.EVT_BUTTON,self.login)
        self.Show()
    def login(self,evt):
            if not self.userName.GetValue():
                   wx.MessageBox(_('Please enter the username'), _('Error'), 
                   wx.OK | wx.ICON_ERROR)
            elif not self.passWord.GetValue():
                    wx.MessageBox(_('Please enter the password'), _('Error'), 
                    wx.OK | wx.ICON_ERROR) 
            else:                 
                 try:
                     db=MySQLdb.connect(host="sql6.freesqldatabase.com",user="sql685198",passwd="jH8*bX3*",db="sql685198",port=3306 )
                     cursor = db.cursor()
                     sql = "SELECT uncompress(password) FROM user WHERE name = '%s' LIMIT 1"%(self.userName.GetValue())
                     cursor.execute(sql)
                     results = cursor.fetchall()
                     if results:
                         for row in results:
                                 password = row[0]
                     else:
                         wx.MessageBox(_('Unable to fecth data,Please check your username'), _('Try it again'), 
                         wx.OK | wx.ICON_ERROR)  
                 except MySQLdb.Error, e:
                       wx.MessageBox('Error %d: %s' % (e.args[0], e.args[1]), _('Try it again'), 
                       wx.OK | wx.ICON_ERROR)  
                 passwd0 = pc.decrypt(password)
                 if self.passWord.GetValue()==passwd0:
                    try:
                        cursor.execute("SELECT uncompress(Data) FROM friendlist WHERE name = '%s' LIMIT 1"%(self.userName.GetValue()))
                        data = json.loads(cursor.fetchone()[0])
                        cursor.close()
                        #conn.close()
                        db.close()
                    except IOError, e:
                          wx.MessageBox('Error %d: %s' % (e.args[0], e.args[1]), 'Try it again', 
                          wx.OK | wx.ICON_ERROR)
                    #urllib2.urlopen('http://chat-tyl.coding.io/user_log?info=User___'+self.userName.GetValue()+'___Login')
                    Notify.init ("Chat-TYL")
                    bubble_notify = Notify.Notification.new (_("Information"),_("Login Successful"),"file://" + os.path.abspath(os.path.curdir) + "/Chat-TYL.ico")
                    bubble_notify.show ()  
                    self.Hide()
                    frame = FriendList.MyFrame(None, id=-1, title=_("Friend List"),user=data,un=self.userName.GetValue())
                    frame.Show(True)
                 else:
                     wx.MessageBox(_('Your Password is wrong'), _('Try it again'), 
                     wx.OK | wx.ICON_ERROR)         
if __name__ == '__main__':
    pc = prpcrypt('keyskeyskeyskeys')
    app = wx.App()
    LoginFrame(None, -1, title = _("Login"), size = (280, 200))
    app.MainLoop()