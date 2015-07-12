#!/usr/bin/python
# encoding: utf-8
import os
import wx
import urllib 
import urllib2 
import sys
import ssl
import FriendList
import Axel
from xml.etree import ElementTree
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
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
        self.passWordLabel = wx.StaticText(self, label = "UserName", pos = (10, 50), size = (120, 25))
        self.userNameLabel = wx.StaticText(self, label = "Password", pos = (40, 100), size = (120, 25))
        self.userName = wx.TextCtrl(self, pos = (120, 47), size = (150, 25))
        self.passWord= wx.TextCtrl(self, pos = (120, 97), size = (150, 25),style=wx.TE_PASSWORD)
        self.loginButton = wx.Button(self, label = 'Login', pos = (80, 145), size = (130, 30))
        self.loginButton.Bind(wx.EVT_BUTTON, self.login)
        self.Show()
    def login(self, event):
            ssl._create_default_https_context = ssl._create_unverified_context
            Axel.paxel('https://7nar2o.com5.z0.glb.clouddn.com/user/' + self.userName.GetValue() + ".xml", self.userName.GetValue() + '.xml', blocks=4, proxies={} )
            response = os.path.exists(self.userName.GetValue()+'.xml')
            if response == 'FALSE':
                wx.MessageBox('Download Error', 'Error', 
                wx.OK | wx.ICON_ERROR)
            else:
                root = ElementTree.fromstring(open(self.userName.GetValue() + ".xml").read())
                node_find = root.find('login')
                pwd_txt = ''.join( [ str(x) for x in node_find.attrib.values()])
                passwd0 = pc.decrypt(pwd_txt)
                if self.passWord.GetValue()==passwd0:
                    urllib2.urlopen('http://chat-tyl.coding.io/user_log?info=User___'+self.userName.GetValue()+'___Login')
                    wx.MessageBox('Login Successful', 'Information', 
                    wx.OK | wx.ICON_INFORMATION)
                    self.Hide()
                    frame = FriendList.MyFrame(None, id=-1, title="Friend List",user=self.userName.GetValue() + '.xml',un=self.userName.GetValue())
                    frame.Show(True)
                else:
                    wx.MessageBox('Your Password is wrong', 'Try it again', 
                    wx.OK | wx.ICON_ERROR) 
if __name__ == '__main__':
    pc = prpcrypt('keyskeyskeyskeys')
    app = wx.App()
    LoginFrame(None, -1, title = "Login", size = (280, 200))
    app.MainLoop()